# 🛡️ Discord Image Guard Bot

A lightweight, fast, and robust Discord bot written in Python that automatically bans users for posting blacklisted images.

It uses a **Hybrid Detection System**:
1. **MD5 Hashing:** Instantly detects exact copies of images (Zero-latency).
2. **ORB (OpenCV):** Detects modified images (cropped, rotated, resized, photographed from a screen).

## 🚀 Features
- **Auto-Ban:** Instantly bans the user upon detection.
- **Auto-Clean:** Deletes user's messages from the last hour (`delete_message_seconds`).
- **Robustness:** Can detect the image even if it's:
    - Rotated or flipped.
    - Photographed with a phone from a monitor.
    - Resized or slightly cropped.
    - Black & White.
- **Non-blocking:** Image processing runs in a separate thread pool, keeping the bot responsive.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lrdcxdes/discord-image-guard.git
   cd discord-image-guard
   ```

2. **Install dependencies:**
   Make sure you have Python 3.8+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   Create a `.env` file in the root directory and add your credentials:
   ```ini
   DISCORD_TOKEN=your_discord_bot_token_here
   ADMIN_ID=123456789012345678
   MATCH_THRESHOLD=20
   ```
   * `MATCH_THRESHOLD`: Lower (10-15) is more sensitive (stricter). Higher (30+) ensures fewer false positives but requires clearer images. 20 is a good balance.

## 🎮 Usage

1. **Run the bot:**
   ```bash
   python main.py
   ```

2. **Add images to the blacklist:**
   - Post an image in Discord (or find one someone posted).
   - Reply to that image with the command: `!bl_add`
   - The bot will download it to `blacklist_photos/` and learn its pattern immediately.

3. **Watch it work:**
   - Any user posting a similar image (even a photo of it taken by a phone) will be banned.

## ⚙️ Technical Details
- **Library:** `discord.py` for API interaction.
- **Computer Vision:** `opencv-python-headless` using the ORB (Oriented FAST and Rotated BRIEF) algorithm combined with Brute-Force Matcher (Hamming distance).
- **Storage:** Images are stored locally in `blacklist_photos/`. Features are cached in RAM for high performance.

## ⚠️ Requirements
- In the Discord Developer Portal, enable **Message Content Intent** and **Server Members Intent**.
- The bot must have **Ban Members** and **Manage Messages** permissions in your server.

## 📝 License
[MIT License](LICENSE)
