import discord
from discord.ext import commands
import logging
from utils.role_check import has_required_role
from typing import Optional

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
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
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
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
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

    @commands.command()
    async def thank(self, ctx, member: discord.Member):
        """Gives the Guinea Pig role to a specified member as a thank you."""
        try:
            guinea_pig_role = discord.utils.get(ctx.guild.roles, name="Guinea Pig")

            if not guinea_pig_role:
                await ctx.send("The 'Guinea Pig' role doesn't exist. Please create it first.")
                return

            if guinea_pig_role in member.roles:
                await ctx.send(f"{member.mention} already has the Guinea Pig role!")
                return

            await member.add_roles(guinea_pig_role)
            embed = discord.Embed(
                title="Thank You!",
                description=f"{member.mention} has been given the Guinea Pig role as a thank you!",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Given by {ctx.author.name}")

            await ctx.send(embed=embed)
            logger.info(f"Guinea Pig role given to user {member.id} by {ctx.author.id}")

        except discord.Forbidden:
            await ctx.send("I don't have permission to manage roles!")
            logger.error("Bot lacks permission to manage roles")
        except Exception as e:
            logger.error(f"Error in thank command: {str(e)}")
            await ctx.send("An error occurred while giving the Guinea Pig role.")

    @commands.command(name="commands")
    async def list_commands(self, ctx):
        """Lists all available commands, their descriptions, and usage format."""
        try:
            embed = discord.Embed(
                title="Available Commands",
                description="Here are all the available commands and their usage:",
                color=discord.Color.blue()
            )

            # List of tuples containing (command_name, description, usage)
            commands_info = [
                ("restrictmod", "Removes Mod-esque role and adds Restricted-Mod role", "!restrictmod @user"),
                ("unrestrictmod", "Removes Restricted-Mod role and adds back Mod-esque role", "!unrestrictmod @user"),
                ("kick", "Kicks a member from the server (requires reason)", "!kick @user <reason>"),
                ("ban", "Bans a member from the server (requires reason)", "!ban @user <reason>"),
                ("thank", "Gives the Guinea Pig role to a specified member", "!thank @user"),
                ("commands", "Lists all available commands and their usage", "!commands")
            ]

            for cmd_name, desc, usage in commands_info:
                embed.add_field(
                    name=f"**{cmd_name}**",
                    value=f"Description: {desc}\nUsage: `{usage}`",
                    inline=False
                )

            embed.set_footer(text="Note: Some commands require specific permissions or roles to use.")
            await ctx.send(embed=embed)
            logger.info(f"Command list displayed for user {ctx.author.id}")

        except Exception as e:
            logger.error(f"Error in list_commands command: {str(e)}")
            await ctx.send("An error occurred while displaying the commands list.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))