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

def help_command():
    print("No help yet fuck off")

async def custom_embed(ctx, title, url, color, thumbnail, description):
    embed = discord.Embed(title=title, url=url, description=description, color=color)
    embed.set_thumbnail(url=thumbnail)
    await ctx.send(embed=embed)


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
        command = input("> ")
        if command is "help":
            help_command()
        elif "custom_embed" in command:
            embed_title = input("custom_embed - title> ")
            embed_url = input("custom_embed - url> ")
            embed_color = input("custom_embed - color> ")
            embed_thumbnail = input("custom_embed - thumbnail> ")
            embed_description = input("custom_embed - description> ")

            if "0x" not in embed_color:
                embed_color = "0x" + embed_color.strip()

            custom_embed(embed_title, embed_url, embed_color, embed_thumbnail, embed_description)


# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
