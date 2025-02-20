import discord
from discord.ext import commands
import logging
import datetime
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.start_time = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')
    
    # Load cogs
    await bot.load_extension('cogs.timing')
    await bot.load_extension('cogs.moderation')
    
    logger.info("All cogs loaded successfully")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command!")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command not found!")
    else:
        logger.error(f"An error occurred: {str(error)}")
        await ctx.send(f"An error occurred: {str(error)}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')
