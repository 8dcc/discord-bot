import discord
from discord.ext import commands

# ---------------------------------------------------------------
# Whitelists and blacklists functions

def check_play_blacklist():
    def predicate(ctx):
        if str(ctx.guild.id) in ctx.bot.play_blacklist:
            return str(ctx.author.id) not in ctx.bot.play_blacklist[str(ctx.guild.id)]
        else:
            return True     # True by default because it's a blacklist
    return commands.check(predicate)

def check_whitelist():
    def predicate(ctx):
        if str(ctx.guild.id) in ctx.bot.whitelist:
            return str(ctx.author.id) in ctx.bot.whitelist[str(ctx.guild.id)]
        else:
            return False
    return commands.check(predicate)

def check_server_admin():
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def check_am_whitelist():
    def predicate(ctx):
        if str(ctx.guild.id) in ctx.bot.am_whitelist:
            return str(ctx.author.id) in am_whitelist[str(ctx.guild.id)]
        else:
            return False
    return commands.check(predicate)

def check_message_blacklist(bot, user_id, guild_id):
    if guild_id in bot.message_log_blacklist:
        return not (str(guild_id) in bot.message_log_blacklist and str(user_id) in bot.message_log_blacklist[str(guild_id)])
    else:
        return True

def check_autoreactions(bot, guild_id, author_id):
    return str(guild_id) in bot.autoreact_list and str(author_id) in bot.autoreact_list[str(guild_id)]

