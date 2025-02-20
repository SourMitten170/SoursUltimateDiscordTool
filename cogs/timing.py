import discord
from discord.ext import commands
import datetime
from utils.time_utils import get_bot_uptime
from utils.role_check import has_required_role
import logging

logger = logging.getLogger('discord_bot')

class Timing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_required_role()
    async def ping(self, ctx):
        """Shows the bot's latency, server time, and uptime"""
        try:
            # Calculate ping
            latency = round(self.bot.latency * 1000)

            # Get current server time
            server_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

            # Get bot uptime
            uptime = get_bot_uptime(self.bot.start_time)

            embed = discord.Embed(title="Bot Status", color=discord.Color.blue())
            embed.add_field(name="Ping", value=f"{latency}ms", inline=False)
            embed.add_field(name="Server Time", value=server_time, inline=False)
            embed.add_field(name="Uptime", value=uptime, inline=False)

            await ctx.send(embed=embed)
            logger.info(f"Ping command executed - Latency: {latency}ms")

        except Exception as e:
            logger.error(f"Error in ping command: {str(e)}")
            await ctx.send("An error occurred while processing the ping command.")

    @commands.command()
    @has_required_role()
    async def test(self, ctx):
        """Shows the operational status of the bot"""
        try:
            embed = discord.Embed(title="Bot Operational Status", color=discord.Color.green())
            embed.add_field(name="Status", value="✅ Operational", inline=False)
            embed.add_field(name="Connected Servers", value=len(self.bot.guilds), inline=False)
            embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)

            await ctx.send(embed=embed)
            logger.info("Test command executed successfully")

        except Exception as e:
            logger.error(f"Error in test command: {str(e)}")
            await ctx.send("An error occurred while processing the test command.")

async def setup(bot):
    await bot.add_cog(Timing(bot))