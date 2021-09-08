import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

##############################
activityType = "Watching"
debug = True
##############################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='n!')  # Your bot prefix
creator_name = "YOUR_NAME#1234"

# ---------------------------------------------------------------

def debug_print(text):
    write_to_log = True  # Will only work if debug is true
    print(text)
    if write_to_log:
        with open("/your/folder/here/discord-bot.log", "a") as discord_log:
            discord_log.write(text + "\n")

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

@client.command()
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
                ydl.download([url])
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
            voice.play(discord.FFmpegPCMAudio("song.mp3"))


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!play <url>`')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)

@client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
        debug_print('Could not find channel for user: %s' % ctx.author)
        return
    else:
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice == None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(ctx.author.voice.channel))
            debug_print('[Bot] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
        else:
            await ctx.send(":warning:  **I am in that channel you fucking piece of shit.** %s" % ctx.author.mention)
            debug_print('[Bot] %s Requested a song, but I am already in that channel.' % ctx.author)
            return


@client.command()
async def leave(ctx):
    voiceChannel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        await ctx.send(":call_me:  **Leaving channel `%s`**" % str(ctx.author.voice.channel))
        debug_print('[Bot] %s requested leave command. Leaving channel %s.' % (str(ctx.author), str(voiceChannel)))
        await voice.disconnect()
        os.remove("song.mp3")
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
        os.remove("song.mp3")
    else:
        await ctx.send(":no_entry_sign:  **The audio is not playing.** %s" % ctx.author.mention)
        debug_print('[Bot] %s Requested stop, but the audio is not playing.' % ctx.author)
        return


# ---------------------------------------------------------------

def check_waifu():
    def predicate(ctx):
        return ctx.author.id == 123123123123123123  # Whitelisted user 1
    return commands.check(predicate)

def check_server_owner():
    def predicate(ctx):
        return ctx.author.id == 123123123123123123  # Whitelisted user 2
    return commands.check(predicate)

@client.command()
@commands.check_any(commands.is_owner(), check_waifu(), check_server_owner())
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been kicked." % member)

@client.command()
@commands.check_any(commands.is_owner(), check_waifu(), check_server_owner())
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been banned." % member)

# ---------------------------------------------------------------

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if debug:
        debug_message = "[%s]-[%s]: %s" % (message.author, message.channel, message.content)
        if "musica" not in str(message.channel).lower():
            debug_print(debug_message)

    if message.content == "ping":
        await message.channel.send("pong")

    if "uwu" in message.content.lower():
        if debug:
            debug_print("[Bot] uwu detected...")
        await message.channel.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        channel = client.get_channel(123123123123123123)  # Channel to send admin messages
        await channel.send("User %s said a forbidden word." % message.author.display_name)

    await client.process_commands(message)

# ---------------------------------------------------------------

try:
    client.run(TOKEN.replace("{","").replace("}",""))  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
