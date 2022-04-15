import discord
from discord.ext import commands

from modules.functions.helpers import *
from modules.functions.checkers import *

class MessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #----------------------------------------------------------------
    # Purge commands

    @commands.command(aliases=["clean"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def purge(self, ctx, member : discord.Member, amount : int):

        def check_purge(check_me):
            return check_me.author.id == member.id

        if amount <= 0:
            embed = discord.Embed(
                    title="Missing arguments",
                    description="**Usage:**  `n!purge <username> <message_amount>`",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [W] [Messages] Could not parse negative integer in purge for user: %s' % ctx.author)
            return

        deleted = await ctx.channel.purge(limit=amount, check=check_purge)

        embed = discord.Embed(
                title="Channel purged",
                description="**%s** removed %s messages by **%s**" % (ctx.author.display_name, len(deleted), member.display_name),
                color=0x11ff11)
        await ctx.send(embed=embed)
        debug_print('[Bot] [Messages] User %s requested purge. Deletd %s messages from user: %s' % (ctx.author, len(deleted), member))

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing arguments",
                    description="**Usage:**  `n!purge <username> <message_amount>`",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found",
                    description="**Make sure you don\'t use nicknames**",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions",
                    description="**You don\'t have the permissions to do that**",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse purge arguments for user: %s' % ctx.author)
        else:
            error_print(error)

    #----------------------------------------------------------------
    # Spam command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def spam(self, ctx, amount : int, *, message2send : str):
        if amount < 1:
            embed = discord.Embed(
                    title="Missing arguments",
                    description="**Usage:**  `n!spam <ammount> <message>`",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse negative integer in spam for user: %s' % ctx.author)
            return

        debug_print('[Bot] [Messages] User %s requested spam. Spamming %s times the message: %s' % (ctx.author, amount, message2send))

        for n in range(amount):
            await ctx.send(message2send)

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing arguments",
                    description="**Usage:**  `n!spam <ammount> <message>`",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse spam arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions",
                    description="**You don\'t have the permissions to do that**",
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Messages] Could not parse arguments for user: %s' % ctx.author)
        else:
            error_print(error)

