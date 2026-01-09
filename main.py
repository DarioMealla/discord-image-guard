import discord
from discord.ext import commands
import aiohttp
import asyncio
import cv2
import numpy as np
import os
import hashlib
import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ImageSentry')

load_dotenv()

class ImageSentry(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        # Configuration
        self.admin_id = int(os.getenv('ADMIN_ID', 0))
        self.match_threshold = int(os.getenv('MATCH_THRESHOLD', 25))
        self.blacklist_dir = 'blacklist_photos'
        
        # Performance
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.session = None
        
        # CV Database
        self.blacklist_features = [] # List of (filename, descriptors)
        self.blacklist_hashes = set() # Set of MD5 strings
        self.orb = cv2.ORB_create(nfeatures=1000)

    async def setup_hook(self):
        """Initialize background tasks and assets before the bot starts."""
        if not os.path.exists(self.blacklist_dir):
            os.makedirs(self.blacklist_dir)
            
        self.session = aiohttp.ClientSession()
        await self.loop.run_in_executor(self.executor, self.load_database)

    def load_database(self):
        """Processes images from disk into RAM for fast matching."""
        temp_features = []
        temp_hashes = set()
        
        files = [f for f in os.listdir(self.blacklist_dir) if os.path.isfile(os.path.join(self.blacklist_dir, f))]
        logger.info(f"Indexing {len(files)} images...")

        for filename in files:
            path = os.path.join(self.blacklist_dir, filename)
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                    temp_hashes.add(hashlib.md5(data).hexdigest())

                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    _, des = self.orb.detectAndCompute(img, None)
                    if des is not None:
                        temp_features.append((filename, des))
            except Exception as e:
                logger.error(f"Failed to index {filename}: {e}")

        self.blacklist_features = temp_features
        self.blacklist_hashes = temp_hashes
        logger.info(f"Database synced: {len(self.blacklist_hashes)} hashes, {len(self.blacklist_features)} descriptors.")

    def _sync_check_image(self, image_bytes):
        """Synchronous CV logic to be run in a thread executor."""
        # 1. Exact MD5 Match
        incoming_hash = hashlib.md5(image_bytes).hexdigest()
        if incoming_hash in self.blacklist_hashes:
            return True, "MD5 Exact Match"

        # 2. Perceptual Matching (ORB)
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_check = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            if img_check is None: return False, None

            _, des_check = self.orb.detectAndCompute(img_check, None)
            if des_check is None: return False, None

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            
            for filename, des_source in self.blacklist_features:
                matches = bf.match(des_check, des_source)
                if len(matches) > self.match_threshold:
                    return True, f"Visual Match ({filename})"
        except Exception as e:
            logger.error(f"CV Processing error: {e}")
            
        return False, None

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.webp')):
                    await self.process_image_attachment(message, attachment)

        await self.process_commands(message)

    async def process_image_attachment(self, message, attachment):
        try:
            async with self.session.get(attachment.url) as resp:
                if resp.status == 200:
                    img_data = await resp.read()
                    is_banned, reason = await self.loop.run_in_executor(
                        self.executor, self._sync_check_image, img_data
                    )

                    if is_banned:
                        await self.apply_sanction(message, reason)
        except Exception as e:
            logger.error(f"Attachment download error: {e}")

    async def apply_sanction(self, message, reason):
        """Deletes message and bans user."""
        try:
            await message.delete()
            await message.guild.ban(
                message.author, 
                reason=f"[Auto-Mod] Blacklisted Image: {reason}",
                delete_message_seconds=3600
            )
            await message.channel.send(
                f"🛡️ **Action Taken**: {message.author.mention} banned for posting prohibited content.",
                delete_after=15
            )
            logger.info(f"Banned {message.author} for {reason}")
        except discord.Forbidden:
            logger.warning(f"Insufficient permissions to ban {message.author}")

    # --- Commands ---

    @commands.command()
    async def bl_add(self, ctx):
        """Adds a replied-to image to the blacklist."""
        if ctx.author.id != self.admin_id: return
        
        if not ctx.message.reference:
            return await ctx.send("❌ Please reply to the image you want to blacklist.")

        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not msg.attachments:
            return await ctx.send("❌ No image found in that message.")

        attachment = msg.attachments[0]
        path = os.path.join(self.blacklist_dir, f"{attachment.id}_{attachment.filename}")

        await attachment.save(path)
        await self.loop.run_in_executor(self.executor, self.load_database)
        await ctx.send(f"✅ Image added to blacklist. Database re-indexed.")

if __name__ == "__main__":
    bot = ImageSentry()
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        logger.error("No token found in .env file.")
