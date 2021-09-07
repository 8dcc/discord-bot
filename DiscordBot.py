import discord, os
from discord.ext import commands
from dotenv import load_dotenv

############################
activityType = "Watching"
debug = True
############################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Replace with your token or whatever

client = commands.Bot(command_prefix='n!')

creator_name = "YOUR_NAME#1234"

def debug_print(text):
    write_to_log = True  # Will only work if debug is true
    print(text)
    if write_to_log:
         with open("discord-bot.log", "a") as discord_log:
             discord_log.write(text)

@client.event
async def on_ready():
    print("---------------------------------------")
    print("The bot has connected to Discord!")
    print("---------------------------------------")
    if activityType is "Playing":
        await client.change_presence(activity=discord.Game(name="with your stepmom"))
    elif activityType is "Watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="lots of gay porn"))
    elif activityType is "Listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="hentai moans"))
    else:
        exit("activityType error. Exiting...")

@client.command()
@commands.is_owner()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been kicked." % member)

@client.command()
@commands.is_owner()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("%s has been banned." % member)

@client.event
async def on_message(message):
    print(client.user)
    if message.author == client.user:
        return

    if debug:
        debug_message = "[%s]-[%s]: %s" % (message.author, message.channel, message.content)
        debug_print(debug_message)

    if message.content == "ping":
        await message.channel.send("pong")

    if "uwu" in message.content.lower():
        if debug:
            debug_print("[Bot] uwu detected...")
        await message.channel.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    await client.process_commands(message)

# Start bot
try:
    client.run(TOKEN.replace("{","").replace("}",""))
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
