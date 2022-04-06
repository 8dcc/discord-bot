import discord, asyncio, json
from discord.ext import commands
import youtube_dl

from modules.functions.helpers import *
from modules.functions.checkers import *

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # ---------------------------------------------------------------
    # Play command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_play_blacklist())
    async def play(self, ctx, *, url : str):

        async def check_alone():
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            while True:
                if voice == None:
                    break
                elif len(voice.channel.members) == 1:
                    await voice.disconnect()
                    await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                    debug_print("[Bot] [Music] Disconnected from channel '%s/%s' because of inactivity." % (str(ctx.guild), str(voice.channel)))
                    break
                await asyncio.sleep(30)

        if ctx.author.voice is None:
            await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] Could not find channel for user: %s' % ctx.author)
        else:
            voiceChannel = ctx.author.voice.channel
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

            if voice is None:
                await voiceChannel.connect()
                await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(ctx.author.voice.channel))
                debug_print('[Bot] [Music] %s requested a song. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
                ctx.bot.loop.create_task(check_alone())

                # Get voice again to play music
                voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                await ctx.send(":information_source:  **Wait for the current audio to end or use the `stop` command**")
                debug_print("[Bot] [W] [Music] %s requested play for \'%s\' but I am playing a song." % (str(ctx.author), url))
                return

            ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': 'true',
                    'max_filesize': 90000000,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }],
                    }

            ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                    }

            if "youtube.com" in url or ".mp3" in url:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                await ctx.send(":musical_note:  **Playing `%s`**" % info_dict['title'])
                debug_print("[Bot] [Music] %s requested play for \'%s\' (%s)." % (str(ctx.author), url, info_dict['title']))
            else:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        get(url)
                    except:
                        info_dict = ydl.extract_info("ytsearch:%s" % url, download=False)['entries'][0]
                    else:
                        info_dict = ydl.extract_info(url, download=False)

                await ctx.send(":musical_note:  **Playing `%s`**" % info_dict['title'])
                debug_print("[Bot] [Music] %s requested play search for \'%s\' (%s)." % (str(ctx.author), url, info_dict['webpage_url']))

            try:
                voice.play(discord.FFmpegPCMAudio(info_dict['url'], **ffmpeg_options))
                voice.is_playing()
            except Exception as e:
                #await ctx.send(":warning: **There was an error playing that song...**")
                embed = discord.Embed(title="Error", 
                        description="**There was an error playing that song.**\nSee possibe errors [here](https://github.com/r4v10l1/discord-bot#possible-errors).", 
                        color=0xff1111)
                await ctx.send(embed=embed)
                error_print(e)


    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(':warning: **Missing required arguments. Usage:**  `n!play <url>`')
            debug_print('[Bot] [E] [Music] Could not parse arguments for user: %s' % ctx.author)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(':warning: **You are in the blacklist, %s.**' % ctx.author.mention)
            debug_print('[Bot] [E] [Music] User %s requested join_channel command, but was in the blacklist.' % ctx.author)
        else:
            embed = discord.Embed(title="Error", 
                    description="**There was an error playing that song.**\nSee possibe errors [here](https://github.com/r4v10l1/discord-bot#possible-errors).", 
                    color=0xff1111)
            await ctx.send(embed=embed)
            error_print(error)

    #----------------------------------------------------------------
    # Join command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_play_blacklist())
    async def join(self, ctx):  # Join the same channel as the user
        if ctx.author.voice is None:
            await ctx.send(":warning:  **I can't find your channel,** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] Could not find channel for user: %s' % ctx.author)
            return

        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(voiceChannel))
            debug_print('[Bot] [Music] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
        else:
            await ctx.send(":warning:  **I am in a channel you fucking piece of shit.** %s" % ctx.author.mention)
            debug_print('[Bot] [E] [Music] %s Requested a song, but I am already in a channel.' % ctx.author)
            return

        async def check_alone():
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            while True:
                if voice == None:
                    break
                elif len(voice.channel.members) == 1:
                    await voice.disconnect()
                    await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                    debug_print("[Bot] [Music] Disconnected from channel '%s/%s' because of inactivity." % (str(ctx.guild), str(voice.channel)))
                    break
                await asyncio.sleep(30)

        ctx.bot.loop.create_task(check_alone())

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':warning: **You are in the blacklist, %s.**' % ctx.author.mention)
            debug_print('[Bot] [W] [Music] User %s requested join command, but he is in the blacklist.' % ctx.author)
        else:
            error_print(error)

    #----------------------------------------------------------------
    # Join_channel command

    @commands.command()
    @commands.check_any(commands.is_owner(), check_play_blacklist())
    async def join_channel(self, ctx, *, channel : str):  # Join custom channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await voiceChannel.connect()
            await ctx.send(":ballot_box_with_check:  **Joined channel `%s`**" % str(voiceChannel))
            debug_print('[Bot] [Music] %s requested join command. Joined channel %s.' % (str(ctx.author), str(voiceChannel)))
        else:
            await ctx.send(":warning:  **I am in that channel you fucking piece of shit.** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] %s Requested a song, but I am already in that channel.' % ctx.author)
            return

        async def check_alone():
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            while True:
                await asyncio.sleep(200)     # Sleep more because it is the join_channel thing
                if voice == None:
                    break
                elif len(voice.channel.members) == 1:
                    await voice.disconnect()
                    await ctx.send(":information_source:  **Left the channel because of inactivity.**")
                    debug_print("[Bot] [Music] Disconnected from channel '%s/%s' because of inactivity." % (str(ctx.guild), str(voice.channel)))
                    break

        ctx.bot.loop.create_task(check_alone())

    @join_channel.error
    async def join_channel_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(':warning: **You are in the blacklist, %s.**' % ctx.author.mention)
            debug_print('[Bot] [W] [Music] User %s requested join_channel command, but he is in the blacklist.' % ctx.author)
        else:
            error_print(error)

    #----------------------------------------------------------------
    # Leave command

    @commands.command()
    async def leave(self, ctx):
        try:
            voiceChannel = ctx.voice_client.channel
        except Exception as e:
            error_print(e)

        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice != None:
            await ctx.send(":call_me:  **Leaving channel `%s`**" % str(voiceChannel))
            debug_print('[Bot] [Music] %s requested leave command. Leaving channel %s.' % (str(ctx.author), str(voiceChannel)))
            await voice.disconnect()
        else:
            await ctx.send(":no_entry_sign:  **I am not in any channel.** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] %s Requested leave, but I am not in a channel.' % ctx.author)
            return

    #----------------------------------------------------------------
    # Pause command

    @commands.command()
    async def pause(self, ctx):
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice != None and voice.is_playing():
            await ctx.send(":pause_button:  **Pausing audio**")
            debug_print('[Bot] [Music] %s requested pause command. Pausing audio...' % str(ctx.author))
            try:
                await voice.pause()
            except:
                pass
        else:
            await ctx.send(":no_entry_sign:  **I am not playing any audio.** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] %s Requested pause, but I am not playing any audio.' % ctx.author)
            return

    #----------------------------------------------------------------
    # Resume command

    @commands.command()
    async def resume(self, ctx):
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice != None and voice.is_paused():
            await ctx.send(":arrow_forward:  **Resuming audio**")
            debug_print('[Bot] [Music] %s requested resume command. Resuming audio...' % str(ctx.author))
            try:
                await voice.resume()
            except:
                pass
        else:
            await ctx.send(":no_entry_sign:  **The audio is not paused.** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] %s Requested resume, but the audio is not paused.' % ctx.author)
            return

    #----------------------------------------------------------------
    # Stop command

    @commands.command()
    async def stop(self, ctx):
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not voice.is_paused() and voice != None:
            await ctx.send(":no_entry:  **Stoping audio**")
            debug_print('[Bot] [Music] %s requested stop command. Stoping audio...' % str(ctx.author))
            try:
                await voice.stop()
            except:
                pass
        else:
            await ctx.send(":no_entry_sign:  **The audio is not playing.** %s" % ctx.author.mention)
            debug_print('[Bot] [W] [Music] %s Requested stop, but the audio is not playing.' % ctx.author)
            return

