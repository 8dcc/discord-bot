import discord, os, time, asyncio, json
from discord.ext import commands
from dotenv import load_dotenv

##############################
debug = True
##############################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = commands.Bot(command_prefix='n!', intents=intents)

discord_log_path = "embed-logs/discord-bot.log"
bot_error_path = "embed-logs/bot-errors.log"
console_settings_path = "settings.json"

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

@commands.command()
async def help():
    print("Edit the configuration file for the custom_embeds!")

# ---------------------------------------------------------------

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the next announcement"))

    with open(console_settings_path, "r") as settings_file:
        json_data = json.loads(settings_file.read())

        print(json.dumps(json_data, indent=4))

        channel_id = json_data['channel_id']
        embed_title = json_data['embed_title']
        embed_url = json_data['embed_url']
        embed_color = json_data['embed_color']
        embed_thumbnail = json_data['embed_thumbnail']
        embed_description = json_data['embed_description']

        if "0x" in embed_color:
            embed_color = embed_color.replace("0x", "")

        await custom_embed(channel_id, embed_title, embed_url, embed_color, embed_thumbnail, embed_description)

# ---------------------------------------------------------------
# Starting the bot

try:
    client.run(TOKEN[1:-1])  # Start bot with the token from .env
except KeyboardInterrupt:
    exit("\nDetected Ctrl+C. Exiting...\n")
