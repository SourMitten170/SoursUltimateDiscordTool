import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord_bot')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

async def setup(bot):
    await bot.add_cog(Moderation(bot))
