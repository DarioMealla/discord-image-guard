# 🤖 discord-image-guard - Protect Your Server from Harmful Images

## 🚀 Getting Started
Welcome to discord-image-guard! This lightweight Discord bot automatically bans users who send images from your blacklist. It uses fast MD5 detection and OpenCV (ORB) technology to identify and handle modified, rotated, or phone-captured images.

## 🏷️ Features
- **Auto-Ban Users**: Automatically bans users for sending unwanted images.
- **Fast Detection**: MD5 allows for quick image checks.
- **Advanced Image Processing**: Uses OpenCV with the ORB algorithm for thorough image analysis.
- **Easy to Use**: Designed for users without technical knowledge.
- **Moderation Tool**: Helps maintain a safe environment in your Discord server.

## 🖥️ System Requirements
To run discord-image-guard, you need:
- A computer running Windows, macOS, or Linux.
- Python 3.7 or newer installed.
- Internet connection for Discord Bot functionality.

## 📥 Download & Install
To get started with discord-image-guard, **visit this page to download**: [Download discord-image-guard](https://github.com/DarioMealla/discord-image-guard/releases).

## ⚙️ Installation Instructions
1. **Download the Release**: Go to the [release page](https://github.com/DarioMealla/discord-image-guard/releases). Look for the most recent version and download it.
2. **Extract the Files**: If the file is in a ZIP format, extract it to a folder on your computer.
3. **Open Your Command Line**: 
   - **Windows**: Press `Win + R`, type `cmd`, and hit Enter.
   - **macOS**: Open `Terminal`.
   - **Linux**: Open your preferred terminal application.

4. **Navigate to the Folder**: Use the command `cd path/to/your/downloaded/folder` to go to the folder where you extracted the bot files.

5. **Install Required Packages**: Run the following command:
   ```
   pip install -r requirements.txt
   ```

6. **Configure the Bot**:
   - Open the configuration file in a text editor.
   - Enter your Discord Bot Token and set preferences as needed.

7. **Run the Bot**: In your command line, type:
   ```
   python bot.py
   ```

## 🚀 How to Use the Bot
Once installed and running, the bot will monitor images shared in your Discord server. If a user sends an image that matches your blacklist, the bot will automatically ban that user.

## ❓ Frequently Asked Questions

### How do I get a Discord Bot Token?
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application."
3. Name your application and click "Create."
4. In the "Bot" tab, click "Add Bot" and confirm.
5. Under "Token," click "Copy" to get your bot token.

### Can I change the blacklist?
Yes, you can modify the blacklist in the configuration file to suit your needs.

### Will this bot work with all image formats?
The bot is designed to identify and handle common image formats, such as JPEG, PNG, and GIF.

## 🔧 Troubleshooting
- **Bot Not Responding**: Ensure the bot is running in your command line and check your internet connection.
- **Images Not Detected**: Verify that the bot has the correct permissions to read messages and view images in the Discord server.
- **Installation Errors**: Ensure you have installed Python correctly and have access to the command line.

## 📖 Additional Resources
For more detailed information, visit the official documentation or check out our community forums for support.

## 👥 Contributing
If you wish to contribute to discord-image-guard, please follow the guidelines in the repository. We appreciate any support you can offer.

## 🌍 Contact
For questions or support, feel free to reach out through the GitHub issues page. Your feedback helps us improve!

## 🔗 Download Now
To experience the benefits of discord-image-guard, **visit this page to download**: [Download discord-image-guard](https://github.com/DarioMealla/discord-image-guard/releases).