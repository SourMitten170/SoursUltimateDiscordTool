from discord.ext import commands
import logging

logger = logging.getLogger('discord_bot')

def has_required_role():
    async def predicate(ctx):
        required_role = "Super Duper Pooper Co-Owner"
        if not any(role.name == required_role for role in ctx.author.roles):
            logger.warning(f"User {ctx.author.id} attempted to use command without required role")
            await ctx.send(f"You need the '{required_role}' role to use this command!")
            return False
        return True
    return commands.check(predicate)
