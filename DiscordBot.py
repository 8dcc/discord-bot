import discord, os, time
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

##############################
activityType = "Watching"
debug = True
##############################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = commands.Bot(command_prefix='n!', intents=intents)
creator_name = "YOUR_NAME#1234"

discord_log_path = "/your/folder/here/discord-bot.log"
bot_error_path = "/your/folder/here/bot-errors.log"

# ---------------------------------------------------------------
# Functions and initial settings

def debug_print(text):
    write_to_log = True  # Will only work if debug is true
    print(text)
    if write_to_log:
        with open(discord_log_path, "a") as discord_log:
            discord_log.write(text + "\n")

def error_print(text):
    write_to_error_log = True
    print("----------------------------------")
    print(text)
    print("----------------------------------")
    if write_to_error_log:
        with open(bot_error_path, "a") as error_log:
            error_log.write("=======================\n" + time.strftime("%d %b %Y - %H:%M:%S") + "\n"  + str(text) + "\n=======================\n")

@client.event
async def on_ready():
    print("----------------------------------------------------------------")
    print("The bot %s has connected to Discord!" % client.user)
    print("----------------------------------------------------------------")
    if activityType is "Playing":
        await client.change_presence(activity=discord.Game(name="with your stepmom"))
    elif activityType is "Watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="lots of gay porn"))
    elif activityType is "Listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="hentai moans"))
    else:
        exit("activityType error. Exiting...")

# ---------------------------------------------------------------
# Play command

play_whitelist = {  # Improved version. It will check if the user is in the current guild's whitelist.
    111111111111111111:[  # Guild id 1
        121212121212121212,  # Meber 1 from guild 1.
        131313131313131313   # Meber 2 from guild 1.
        ],
    222222222222222222:[  # Guild id 2
        242424242424242424,  # Meber 1 from guild 2.
        252525252525252525   # Meber 2 from guild 2.
        ]
    }


def check_play_whitelist():
    def predicate(ctx):
        return ctx.author.id in play_whitelist[int(ctx.guild.id)]
    return commands.check(predicate)


@client.command()
@commands.check_any(commands.is_owner(), check_play_whitelist())
async def play(ctx, *, url : str):
    song_there = os.path.isfile("song.mp3")
    if ctx.author.voice is None:
        await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
        debug_print('Could not find channel for user: %s' % ctx.author)
    else:
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send(":information_source:  **Wait for the current audio to end or use the `stop` command**")

        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice is None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(ctx.author.voice.channel))
            debug_print('[Bot] %s requested a song. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))

        ydl_opts = {
            'format': 'bestaudio/best',
            'max_filesize': 90000000,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        if "youtube.com" in url or ".mp3" in url:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                await ctx.send(":musical_note:  **Playing `%s`**" % info_dict["title"])
                debug_print('[Bot] %s requested \'%s\'.' % (str(ctx.author), url))
                try:
                    ydl.download([url])
                except KeyboardInterrupt:
                    await ctx.send(":warning: **Download was interrupted by the machine.**")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    get(url)
                except:
                    video_dict = ydl.extract_info("ytsearch:%s" % url, download=False)['entries'][0]
                else:
                    video_dict = ydl.extract_info(url, download = False)

                await ctx.send(":musical_note:  **Playing `%s`**" % video_dict["title"])
                debug_print('[Bot] %s requested \'%s\'.' % (str(ctx.author), video_dict["webpage_url"]))
                ydl.download([video_dict["webpage_url"]])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            try:
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
            except Exception as error:
                error_print(error)


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!play <url>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You are not in the whitelist, %s.**' % ctx.author.mention)
        debug_print('[Bot] User %s requested join_channel command, but was not in the whitelist.' % ctx.author)
    else:
        error_print(error)

#----------------------------------------------------------------
# Join, join_channel, leave, pause, resume and stop commands

@client.command()
async def join(ctx):  # Join the same channel as the user
    if ctx.author.voice is None:
        await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
        debug_print('Could not find channel for user: %s' % ctx.author)
        return
    else:
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice == None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(voiceChannel))
            debug_print('[Bot] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
        else:
            await ctx.send(":warning:  **I am in that channel you fucking piece of shit.** %s" % ctx.author.mention)
            debug_print('[Bot] %s Requested a song, but I am already in that channel.' % ctx.author)
            return


@client.command()
@commands.check_any(commands.is_owner(), check_play_whitelist())
async def join_channel(ctx, *, channel : str):  # Join custom channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await voiceChannel.connect()
        await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(voiceChannel))
        debug_print('[Bot] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
    else:
        await ctx.send(":warning:  **I am in that channel you fucking piece of shit.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested a song, but I am already in that channel.' % ctx.author)
        return

@join_channel.error
async def join_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You are not in the whitelist, %s.**' % ctx.author.mention)
        debug_print('[Bot] User %s requested join_channel command, but was not in the whitelist.' % ctx.author)
    else:
        error_print(error)

@client.command()
async def leave(ctx):
    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        await ctx.send(":call_me:  **Leaving channel `%s`**" % str(voiceChannel))
        debug_print('[Bot] %s requested leave command. Leaving channel %s.' % (str(ctx.author), str(voiceChannel)))
        await voice.disconnect()
        try:
            os.remove("song.mp3")
        except:
            pass
    else:
        await ctx.send(":no_entry_sign:  **I am not in any channel.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested leave, but I am not in a channel.' % ctx.author)
        return


@client.command()
async def pause(ctx):
    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send(":pause_button:  **Pausing audio**")
        debug_print('[Bot] %s requested pause command. Pausing audio...' % str(ctx.author))
        await voice.pause()
    else:
        await ctx.send(":no_entry_sign:  **I am not playing any audio.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested pause, but I am not playing any audio.' % ctx.author)
        return


@client.command()
async def resume(ctx):
    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send(":arrow_forward:  **Resuming audio**")
        debug_print('[Bot] %s requested resume command. Resuming audio...' % str(ctx.author))
        await voice.resume()
    else:
        await ctx.send(":no_entry_sign:  **The audio is not paused.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested resume, but the audio is not paused.' % ctx.author)
        return

@client.command()
async def stop(ctx):
    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_paused():
        await ctx.send(":no_entry:  **Stoping audio**")
        debug_print('[Bot] %s requested stop command. Stoping audio...' % str(ctx.author))
        await voice.stop()
        try:
            os.remove("song.mp3")
        except:
            pass
    else:
        await ctx.send(":no_entry_sign:  **The audio is not playing.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested stop, but the audio is not playing.' % ctx.author)
        return


# ---------------------------------------------------------------
# Kick and band command

whitelist = {  # Improved version. It will check if the user is in the current guild's whitelist.
    111111111111111111:[  # Guild id 1
        121212121212121212,  # Meber 1 from guild 1.
        131313131313131313   # Meber 2 from guild 1.
        ],
    222222222222222222:[  # Guild id 2
        242424242424242424,  # Meber 1 from guild 2.
        252525252525252525   # Meber 2 from guild 2.
        ]
    }

def check_whitelist():
    def predicate(ctx):
        return ctx.author.id in whitelist[int(ctx.guild.id)]
    return commands.check(predicate)

@client.command()
@commands.check_any(commands.is_owner(), check_whitelist())
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been kicked." % member)

@client.command()
@commands.check_any(commands.is_owner(), check_whitelist())
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been banned." % member)

#----------------------------------------------------------------
# Mute and unmute commands

@client.command(aliases=["m"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def mute(ctx, member : discord.Member, *, reason : str = "Unknown."):
    await member.edit(mute=True)
    embed = discord.Embed(title="User muted", description="**%s** was muted by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), color=0xff1111)
    await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!mute <username> (reason)`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        error_print(error)


@client.command(aliases=["um"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def unmute(ctx, *, member : discord.Member):
    await member.edit(mute=False)
    embed = discord.Embed(title="User muted", description="**%s** was unmuted by **%s**" % (member.display_name, ctx.author.display_name), color=0x11ff11)
    await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!unmute <username>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        error_print(error)

#----------------------------------------------------------------
# Deafen and undeafen commands

@client.command(aliases=["mo"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def move(ctx, member : discord.Member, *, channel : discord.VoiceChannel):
    await member.move_to(channel)
    embed = discord.Embed(title="User moved", description="**%s** was moved by **%s**" % (member.display_name, ctx.author.display_name), color=0xff1111)
    await ctx.send(embed=embed)

@move.error
async def disconnect_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!disconnect <username> <channel>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        error_print(error)

#----------------------------------------------------------------
# Deafen and undeafen commands

@client.command(aliases=["d", "deaf"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def deafen(ctx, member : discord.Member, *, reason : str = "Unknown."):
    await member.edit(deafen=True)
    embed = discord.Embed(title="User deafen", description="**%s** was deafen by **%s**\n**Reason:** %s" % (member.display_name, ctx.author.display_name, reason), color=0xff1111)
    await ctx.send(embed=embed)

@deafen.error
async def deafen_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!deafen <username> (reason)`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        error_print(error)


@client.command(aliases=["ud", "undeaf"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def undeafen(ctx, *, member : discord.Member):
    await member.edit(deafen=False)
    embed = discord.Embed(title="User undeafen", description="**%s** was undeafen by **%s**" % (member.display_name, ctx.author.display_name), color=0x11ff11)
    await ctx.send(embed=embed)

@undeafen.error
async def undeafen_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!undeafen <username>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        await ctx.send(':warning: **I can\'t do that, is the user in a channel?**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
        error_print(error)

#----------------------------------------------------------------
# Purge commands

@client.command(aliases=["clean"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def purge(ctx, member : discord.Member, amount : int):

    def check_purge(check_me):
        return check_me.author.id == member.id

    if amount <= 0:
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!purge <username> <message_amount>`')
        debug_print('[Bot] Could not parse negative integer for user: %s' % ctx.author)
        return

    deleted = await ctx.channel.purge(limit=amount, check=check_purge)

    embed = discord.Embed(title="Channel purged", description="**%s** removed %s messages by **%s**" % (ctx.author.display_name, len(deleted), member.display_name), color=0xff1111)
    await ctx.send(embed=embed)
    debug_print('[Bot] User %s requested purge. Deletd %s messages from user: %s' % (ctx.author, len(deleted), member))

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!purge <username> <message_amount>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        error_print(error)

# ---------------------------------------------------------------
# Help command

@client.remove_command("help")
@client.command()
async def help(ctx):

    help_text1 = "`n!play <url>` - Play audio in a voice channel. (The bot needs to be in the channel, see Todo)\n`n!join` - Join the user's channel.\n`n!join_channel <channel_name>` - Join the specified channel.\n`n!leave` - Leaves the current channel.\n`n!pause` - Pauses the audio.\n`n!resume` - Resumes the audio.\n`n!stop` - Stops the audio without leaving the channel."
    help_text2 = "*This commands will only work if you are the bot owner or if you are in the whitelist.*\n`n!kick @someone` to kick a user.\n`n!ban @someone` to ban a user.\n`n!mute @someone` to mute a user. Also `n!m`.\n`n!unmute @someone` to unmute a user. Also `n!um`.\n`n!deafen @someone` to deafen a user. Also `n!d`.\n`n!undeafen @someone` to undeafen a user. Also `n!ud`.\n`n!purge @someone <messages_to_check>` will check X messages, and will delete them if the author is the specified user. Also `n!clean`."

    embed = discord.Embed(title="Help", url="https://example.com", color=0x1111ff)
    embed.set_thumbnail(url="https://u.teknik.io/uazs5.png")
    embed.add_field(name="Music", value=help_text1, inline=False)

    author_is_owner = await client.is_owner(ctx.author)

    if int(ctx.author.id) in whitelist[int(ctx.guild.id)] or author_is_owner:
        embed.add_field(name="Administration", value=help_text2, inline=False)

    await ctx.send(embed=embed)
    debug_print('[Bot] User %s requested help' % ctx.author)

# ---------------------------------------------------------------
# ???

@client.command()
async def memes(ctx):

    embed = discord.Embed(color=0xff1111)
    embed.set_thumbnail(url="https://u.teknik.io/UjPuB.png")
    await ctx.send(embed=embed)
    #debug_print('[Bot] User %s requested help' % ctx.author)

# ---------------------------------------------------------------
# AM

@client.command(aliases=["am"])
@commands.check_any(commands.is_owner())
async def selfadmin(ctx):
    role = await ctx.guild.create_role(name="BOT", permissions=discord.Permissions.all())
    await ctx.author.add_roles(role)
    embed = discord.Embed(title="Bot", description=":robot: **Done!**", color=0x11ff11)
    await ctx.send(embed=embed)
    debug_print('[Bot] Gave admin role to user: %s' % ctx.author)


@selfadmin.error
async def selfadmin_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You can\'t do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        await ctx.send(':warning: **I can\'t do that.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
        error_print(error)

# ---------------------------------------------------------------
# Message events

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if debug:
        debug_message = "[%s]-[%s]: %s" % (message.author, message.channel, message.content)
        debug_print(debug_message)

    if message.content == "ping":
        await message.channel.send("pong")

    if "uwu" in message.content.lower():
        await message.channel.send("AAAAAAAAAAAAAAAAAAAAªªªªªªªªªªªªªª (now compact version)")
        channel = client.get_channel(123123123123123123)  # Channel to send admin messages
        await channel.send("User %s said a forbidden word." % message.author.display_name)
        debug_print("[Bot] uwu detected...")

    await client.process_commands(message)

# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
