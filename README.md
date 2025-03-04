# Discord Moderation Bot

A Discord bot with timing commands and mod role management functionality.

## Features

- Moderation Commands
  - Restrict/Unrestrict moderators
  - Kick members
  - Ban members
  - Thank users (assigns Guinea Pig role)
- Timing Commands
  - Ping (shows latency and uptime)
  - Test (shows operational status)
- Command List
  - View all available commands and their usage

## Setup

1. Install Python 3.11 or later
 ```
   sudo apt install python3.11 -y
```
3. Install required packages (Ubuntu 24.10):
```
sudo pip install --break-system-packages "discord.py>=2.5.0" "Flask>=3.1.0" "Flask-Login>=0.6.3" "Flask-WTF>=1.2.2" "twilio>=9.4.6"
  ```
3. Create a Discord bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Add a bot to your application
   - Copy the bot token

4. Set up environment variables:
   - Create a `.env` file or set the environment variable:
     ```
     DISCORD_BOT_TOKEN=your_bot_token_here
     ```

5. Configure the bot:
   - Update `TARGET_GUILD_ID` in `bot.py` with your server ID
   - Ensure all required roles exist in your server:
     - "Super Duper Pooper Co-Owner" (for command access)
     - "Mod-esque" (for moderation)
     - "Restricted-Mod" (for restricted moderators)
     - "Guinea Pig" (for thank command)

change the role names to the role names you use.

6. Run the bot:
   ```bash
   python bot.py
   ```

## Required Permissions

The bot needs the following permissions:
- Manage Roles
- Kick Members
- Ban Members
- Send Messages
- Read Messages
- View Channels
- Embed Links

## Project Structure

```
project_root/
├── cogs/
│   ├── moderation.py  # Moderation commands
│   └── timing.py      # Timing-related commands
├── utils/
│   ├── logger.py      # Logging configuration
│   ├── role_check.py  # Role verification
│   └── time_utils.py  # Time calculation utilities
├── bot.py             # Main bot file
└── pyproject.toml     # Project dependencies
```
