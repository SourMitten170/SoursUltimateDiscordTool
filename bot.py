import discord
from discord.ext import commands, tasks
import logging
import datetime
from utils.logger import setup_logger
import os
from keep_alive import keep_alive
import subprocess

# Set up logging
logger = setup_logger()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.start_time = datetime.datetime.utcnow()

TARGET_GUILD_ID = 1335980477466546250

@tasks.loop(hours=6)
async def update_repository():
    """Updates the GitHub repository every 6 hours"""
    try:
        # Check if git is configured
        try:
            email = subprocess.check_output(['git', 'config', '--get', 'user.email']).decode().strip()
            name = subprocess.check_output(['git', 'config', '--get', 'user.name']).decode().strip()
        except subprocess.CalledProcessError:
            logger.error("Git user not configured. Auto-update disabled.")
            return

        # Perform the update
        subprocess.run(['git', 'add', '.'], check=True)
        commit_message = f'Auto-update: {datetime.datetime.now()}'
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        logger.info(f"Successfully updated GitHub repository with message: {commit_message}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to update repository: {str(e)}")

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')

    # Generate invite link with required permissions
    permissions = discord.Permissions()
    permissions.manage_roles = True    # For role management commands
    permissions.kick_members = True    # For kick command
    permissions.ban_members = True     # For ban command
    permissions.send_messages = True   # For sending command responses
    permissions.read_messages = True   # For reading commands
    permissions.view_channel = True    # For seeing channels
    permissions.embed_links = True     # For sending embeds

    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=permissions,
        scopes=["bot"]
    )

    logger.info(f"Invite the bot to your server using this link:\n{invite_link}")

    # Check if bot is in the target guild
    target_guild = bot.get_guild(TARGET_GUILD_ID)
    if target_guild:
        logger.info(f"Successfully connected to target server: {target_guild.name}")
    else:
        logger.warning(f"Bot is not in the target server (ID: {TARGET_GUILD_ID}). Please use the invite link above to add the bot.")

    # Load cogs
    await bot.load_extension('cogs.timing')
    await bot.load_extension('cogs.moderation')

    # Start repository update task
    update_repository.start()

    logger.info("All cogs loaded successfully")

@bot.event
async def on_guild_join(guild):
    if guild.id == TARGET_GUILD_ID:
        logger.info(f"Bot has joined the target server: {guild.name}")
    else:
        logger.warning(f"Bot joined an unexpected server: {guild.name} ({guild.id})")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command!")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command not found!")
    else:
        logger.error(f"An error occurred: {str(error)}")
        await ctx.send(f"An error occurred: {str(error)}")

# Get the token from environment variables
token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    logger.error("No Discord bot token found in environment variables!")
    raise ValueError("Discord bot token not found")

# Start the keep-alive server
keep_alive()

# Run the bot
bot.run(token)