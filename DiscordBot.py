try:
    import discord, os, time, asyncio, json, emoji, git
    from discord.ext import commands
    from dotenv import load_dotenv
except Exception:
    print("Could not load modules. Make sure you run:")
    print("python3 -m pip install -r requirements.txt")

import modules.variables.custom_emotes as custom_emotes
from settings import *

import modules.functions.botclass as botclass
from modules.functions.helpers import *
from modules.functions.checkers import *

from modules.cogs.music import *
from modules.cogs.administration import *
from modules.cogs.messages import *
from modules.cogs.am import *
from modules.cogs.ping import *

# ---------------------------------------------------------------
# Get token and start bot

check_defaults()
TOKEN = get_env_token()

intents = discord.Intents().all()
client = botclass.MyBot(command_prefix='n!', intents=intents)
client.cache_data()

# ---------------------------------------------------------------
# When the bot loads

@client.event
async def on_ready():
    print("----------------------------------------------------------------")
    print("The bot %s has connected to Discord!" % client.user)
    print("----------------------------------------------------------------")
    if activityType == "Playing":
        await client.change_presence(activity=discord.Game(name="with your stepmom"))
    elif activityType == "Watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="n!help"))
    elif activityType == "Listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="n!help"))
    else:
        exit("activityType error. Exiting...")

# ---------------------------------------------------------------
# Add cogs

# Play, join, join_channel, leave, pause, resume and stop commands
client.add_cog(MusicCog(client))
# Kick, ban, move, deafen, undeafen commands
client.add_cog(AdministrationCog(client))
# Autoreactions
#client.add_cog(MusicCog(client))
# Purge, spam and memes commands
client.add_cog(MessagesCog(client))
# AM command
client.add_cog(AmCog(client))
# Ping command
client.add_cog(PingCog(client))

# ---------------------------------------------------------------
# Help command

# Can't get this (remove_command) to work in a cog, feel free to improve it
@client.command()
async def help(ctx):

    help_text1 = "`n!play <url>` - Play audio in a voice channel (.mp3 url, youtube url or youtube search). \n`n!join` - Join the user's channel.\n`n!join_channel <channel_name>` - Join the specified channel.\n`n!leave` - Leaves the current channel.\n`n!pause` - Pauses the audio.\n`n!resume` - Resumes the audio.\n`n!stop` - Stops the audio without leaving the channel."
    help_text2 = "*This commands will only work if you are the bot owner or if you are in the whitelist.*\n`n!kick @someone` to kick a user.\n`n!ban @someone` to ban a user.\n`n!mute @someone` to mute a user. Also `n!m`.\n`n!unmute @someone` to unmute a user. Also `n!um`.\n`n!deafen @someone` to deafen a user. Also `n!d`.\n`n!undeafen @someone` to undeafen a user. Also `n!ud`.\n`n!purge @someone <messages_to_check>` will check X messages, and will delete them if the author is the specified user. Also `n!clean`.\n`n!spam <amount> <message>` will spam the specified messae in the current channel the amount of times."

    embed = discord.Embed(title="Help", 
            url="https://github.com/r4v10l1/discord-bot/blob/main/README.md", 
            color=0x1111ff)
    embed.set_thumbnail(url="https://u.teknik.io/m3lTR.png")
    embed.add_field(name="Music", 
            value=help_text1, 
            inline=False)

    isowner = await client.is_owner(ctx.author)     # Needs a variable so we can await

    if (isowner) or ( (int(ctx.guild.id) in client.whitelist) and (int(ctx.author.id) in client.whitelist[int(ctx.guild.id)]) ):
        embed.add_field(name="Administration",
                value=help_text2,
                inline=False)

    await ctx.send(embed=embed)
    debug_print('[Bot] [Help] User %s requested help' % ctx.author)

# ---------------------------------------------------------------
# Message events

@client.event
async def on_message(message):
    if message.author == client.user or message.content.strip() == "":
        return

    if debug and check_message_blacklist(client, message.author.id, message.author.guild.id):
        try:
            debug_message = "[%s/%s]-[%s]: %s" % (message.author.guild.name, message.channel, message.author, message.content)
            debug_print(debug_message)
        except Exception:
            pass

    if message.content == "ping":
        await message.channel.send("pong")

    if check_autoreactions(client, message.author.guild.id, message.author.id):
        full_reaction_str = ""
        reaction_array = client.autoreact_list[str(message.author.guild.id)][str(message.author.id)]

        for reaction_name in reaction_array:
            if ":regional_indicator_" in reaction_name:
                emote = custom_emotes.get_regional_emoji(reaction_name)
            elif ":" in reaction_name.strip():
                emote = emoji.emojize(str(reaction_name), language='alias')
                if emote == reaction_name.strip():
                    emote = emoji.emojize(str(reaction_name), language='en')
            else:
                emote = reaction_name

            try:
                await message.add_reaction(emote)
                full_reaction_str += reaction_name + ","
            except Exception:
                pass

        if len(reaction_array) > 0:
            debug_print("[Bot] [Reactions] Added reactions (%s) for user %s." % (full_reaction_str[:-1], message.author))

    if "uwu-is-disabled" in message.content.lower():
        if debug:
            debug_print("[Bot] [Message detection] uwu detected...")
        embed = discord.Embed(title="Tourette", description="**AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA**\n Can't say that here.", color=0xff1111)
        await message.channel.send(embed=embed)
        channel = client.get_channel(12312312312312313123)
        if channel != None:
            await channel.send("[Alert] User %s said something bad." % message.author)

    await client.process_commands(message)

# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])     # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
