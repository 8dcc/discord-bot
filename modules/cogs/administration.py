import discord
from discord.ext import commands

from modules.functions.helpers import *
from modules.functions.checkers import *

class AdministrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # ---------------------------------------------------------------
    # Kick command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
                title="User kicked", 
                description="**%s** was kicked by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), 
                color=0xff1111)
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!kick <username> (reason)`",  
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse kick arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don't use nicknames**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse kick arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse kick arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="I can't do that!", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)

    # ---------------------------------------------------------------
    # Ban command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
                title="User banned", 
                description="**%s** was banned by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), 
                color=0x11ff11)
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!ban <username> (reason)`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse ban arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nicknames**",  
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse ban arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**",  
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse ban arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="I can't do that!", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)

    #----------------------------------------------------------------
    # Mute command

    @commands.command(aliases=["m"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def mute(self, ctx, member : discord.Member, *, reason : str = "Unknown."):
        await member.edit(mute=True)
        embed = discord.Embed(
                title="User muted", 
                description="**%s** was muted by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), 
                color=0x11ff11)
        await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!mute <username> (reason)`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nickname**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="I can't do that!", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)

    #----------------------------------------------------------------
    # Unmute command

    @commands.command(aliases=["um"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def unmute(self, ctx, *, member : discord.Member):
        await member.edit(mute=False)
        embed = discord.Embed(
                title="User muted", 
                description="**%s** was unmuted by **%s**" % (member.display_name, ctx.author.display_name), 
                color=0x11ff11)
        await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!unmute <username>`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nicknames**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="I can't do that!", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)

    #----------------------------------------------------------------
    # Deafen command

    @commands.command(aliases=["d", "deaf"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def deafen(self, ctx, member : discord.Member, *, reason : str = "Unknown."):
        await member.edit(deafen=True)
        embed = discord.Embed(
                title="User deafen", 
                description="**%s** was deafen by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), 
                color=0xff1111)
        await ctx.send(embed=embed)

    @deafen.error
    async def deafen_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!deafen <username> (reason)`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nicknames**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="I can't do that!", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)


    #----------------------------------------------------------------
    # Undeafen command

    @commands.command(aliases=["ud", "undeaf"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def undeafen(self, ctx, *, member : discord.Member):
        await member.edit(deafen=False)
        embed = discord.Embed(
                title="User undeafen", 
                description="**%s** was undeafen by **%s**" % (member.display_name, ctx.author.display_name), 
                color=0x11ff11)
        await ctx.send(embed=embed)

    @undeafen.error
    async def undeafen_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!undeafen <username>`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nicknames.**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        else:
            embed = discord.Embed(
                    title="Error", 
                    description="**I can\'t do that, is the user in a channel?**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
            error_print(error)

    #----------------------------------------------------------------
    # Move command

    @commands.command(aliases=["mo"])
    @commands.check_any(commands.is_owner(), check_whitelist())
    async def move(self, ctx, member : discord.Member, *, channel : discord.VoiceChannel):
        await member.move_to(channel)
        embed = discord.Embed(
                title="User moved", 
                description="**%s** was moved by **%s**" % (member.display_name, ctx.author.display_name), 
                color=0xff1111)
        await ctx.send(embed=embed)

    @move.error
    async def disconnect_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    title="Missing required arguments", 
                    description="**Usage:** `n!disconnect <username> <channel>`", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                    title="Member not found", 
                    description="**Make sure you don\'t use nicknames.**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                    title="Missing permissions", 
                    description="**You don\'t have the permissions to do that**", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            debug_print('[Bot] [E] [Admin] Could not parse arguments for user: %s' % ctx.author)
        else:
            error_print(error)

