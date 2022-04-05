import discord
from discord.ext import commands

from modules.functions.helpers import *
from modules.functions.checkers import *

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.add_reaction("\U0001f44b")
        debug_print('[Bot] User %s requested ping command.' % ctx.author)

    @commands.command()
    async def memes(self, ctx):
        embed = discord.Embed(color=0xff1111)
        embed.set_thumbnail(url="https://u.teknik.io/UjPuB.png")
        await ctx.send(embed=embed)
