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

# ---------------------------------------------------------------
# Help command

async def help_command():
    print("No help yet fuck off")

async def custom_embed(channel_id, title, url, color, thumbnail, description):
    color = discord.Color(value=int(color, 16))

    embed = discord.Embed(title=title, url=url, description=description, color=color)
    embed.set_thumbnail(url=thumbnail)

    channel = client.get_channel(int(channel_id))
    await channel.send(embed=embed)


# ---------------------------------------------------------------
# Main

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

    while True:
        try:
            command = input("> ")
        except KeyboardInterrupt:
            exit(1)
        if command is "help":
            help_command()
        elif "custom_embed" in command:
            channel_id = input("custom_embed - channel_id> ")
            embed_title = input("custom_embed - title> ")
            embed_url = input("custom_embed - url> ")
            embed_color = input("custom_embed - color> ")
            embed_thumbnail = input("custom_embed - thumbnail> ")
            embed_description = input("custom_embed - description> ")

            if "0x" in embed_color:
                embed_color = embed_color.replace("0x", "")

            await custom_embed(channel_id, embed_title, embed_url, embed_color, embed_thumbnail, embed_description)
        elif "clear" in command:
            os.system("clear")
        elif "exit" in command:
            exit(1)
        else:
            print("Unknown command.")


# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
