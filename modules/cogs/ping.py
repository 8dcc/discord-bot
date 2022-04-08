import discord, git
from discord.ext import commands

from modules.functions.helpers import *
from modules.functions.checkers import *
import modules.variables.custom_colors as custom_colors

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # ---------------------------------------------------------------
    # Ping command

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.add_reaction("\U0001f44b")
        debug_print('[Bot] [Ping] User %s requested ping command.' % ctx.author)

    # ---------------------------------------------------------------
    # Ping command

    @commands.command()
    async def memes(self, ctx):
        embed = discord.Embed(color=0xff1111)
        embed.set_thumbnail(url="https://u.teknik.io/UjPuB.png")
        await ctx.send(embed=embed)
        debug_print('[Bot] [Ping] User %s requested memes command.' % ctx.author)

    # ---------------------------------------------------------------
    # Version command

    @commands.command(aliases=["ver"])
    async def version(self, ctx):
        repo = git.Repo(search_parent_directories=True)
        repo.remotes.origin.fetch()     # Fetches the remote information instead of using the local info on origin

        head_hash = repo.head.object.hexsha                         # Check the last head commit
        origin_hash = repo.remotes.origin.refs.main.object.hexsha   # Check the last origin/main commit
        # origin_hash = repo.remotes.origin.refs[0].object.hexsha   # Check the last origin/head commit

        if head_hash == origin_hash:
            origin_emote = ":white_check_mark:"
        else:
            origin_emote = ":x:"

        head_description = f":whale: [`{head_hash}`](https://github.com/r4v10l1/discord-bot/commit/{head_hash})\n"
        origin_description = f"{origin_emote} [`{origin_hash}`](https://github.com/r4v10l1/discord-bot/commit/{origin_hash})",
        embed = discord.Embed(title = "Version", 
                url = "https://github.com/r4v10l1/discord-bot/commits/main",
                description = head_description + origin_descriptiont, 
                color = custom_colors.DEFAULT_EMBED)

        await ctx.send(embed=embed)
        debug_print('[Bot] [Ping] User %s requested version command.' % ctx.author)

    # ---------------------------------------------------------------
    # Stats command?
