import discord
from discord.ext import commands
import logging
from utils.role_check import has_required_role

logger = logging.getLogger('discord_bot')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_required_role()
    @commands.has_permissions(manage_roles=True)
    async def restrictmod(self, ctx, member: discord.Member):
        """Removes Mod-esque role and adds Restricted-Mod role"""
        try:
            mod_role = discord.utils.get(ctx.guild.roles, name="Mod-esque")
            restricted_role = discord.utils.get(ctx.guild.roles, name="Restricted-Mod")

            if not mod_role or not restricted_role:
                await ctx.send("Required roles not found. Please ensure both 'Mod-esque' and 'Restricted-Mod' roles exist.")
                return

            if mod_role in member.roles:
                await member.remove_roles(mod_role)
                await member.add_roles(restricted_role)
                await ctx.send(f"Successfully restricted moderator permissions for {member.mention}")
                logger.info(f"Restricted mod permissions for user {member.id}")
            else:
                await ctx.send(f"{member.mention} doesn't have the Mod-esque role.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to manage roles!")
            logger.error("Bot lacks permission to manage roles")
        except Exception as e:
            logger.error(f"Error in restrictmod command: {str(e)}")
            await ctx.send("An error occurred while restricting moderator permissions.")

    @commands.command()
    @has_required_role()
    @commands.has_permissions(manage_roles=True)
    async def unrestrictmod(self, ctx, member: discord.Member):
        """Removes Restricted-Mod role and adds back Mod-esque role"""
        try:
            mod_role = discord.utils.get(ctx.guild.roles, name="Mod-esque")
            restricted_role = discord.utils.get(ctx.guild.roles, name="Restricted-Mod")

            if not mod_role or not restricted_role:
                await ctx.send("Required roles not found. Please ensure both 'Mod-esque' and 'Restricted-Mod' roles exist.")
                return

            if restricted_role in member.roles:
                await member.remove_roles(restricted_role)
                await member.add_roles(mod_role)
                await ctx.send(f"Successfully unrestricted moderator permissions for {member.mention}")
                logger.info(f"Unrestricted mod permissions for user {member.id}")
            else:
                await ctx.send(f"{member.mention} doesn't have the Restricted-Mod role.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to manage roles!")
            logger.error("Bot lacks permission to manage roles")
        except Exception as e:
            logger.error(f"Error in unrestrictmod command: {str(e)}")
            await ctx.send("An error occurred while unrestricting moderator permissions.")

    @commands.command()
    @has_required_role()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a member from the server. Reason is required."""
        try:
            if not reason:
                await ctx.send("You must provide a reason for kicking the member.")
                return

            if member.top_role >= ctx.author.top_role:
                await ctx.send("You cannot kick someone with a role higher than or equal to yours.")
                return

            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked from the server.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Kicked by", value=ctx.author.mention)

            await ctx.send(embed=embed)
            logger.info(f"User {member.id} was kicked by {ctx.author.id} for reason: {reason}")

        except discord.Forbidden:
            await ctx.send("I don't have permission to kick members!")
            logger.error("Bot lacks permission to kick members")
        except Exception as e:
            logger.error(f"Error in kick command: {str(e)}")
            await ctx.send("An error occurred while trying to kick the member.")

    @commands.command()
    @has_required_role()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bans a member from the server. Reason is required."""
        try:
            if not reason:
                await ctx.send("You must provide a reason for banning the member.")
                return

            if member.top_role >= ctx.author.top_role:
                await ctx.send("You cannot ban someone with a role higher than or equal to yours.")
                return

            await member.ban(reason=f"Banned by {ctx.author}: {reason}", delete_message_days=1)
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned from the server.",
                color=discord.Color.dark_red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Banned by", value=ctx.author.mention)

            await ctx.send(embed=embed)
            logger.info(f"User {member.id} was banned by {ctx.author.id} for reason: {reason}")

        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members!")
            logger.error("Bot lacks permission to ban members")
        except Exception as e:
            logger.error(f"Error in ban command: {str(e)}")
            await ctx.send("An error occurred while trying to ban the member.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))