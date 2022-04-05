import discord, json
from discord.ext import commands

import settings

# ---------------------------------------------------------------
# Main bot (Helpers)

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ---------------------------------------------------------------
    # Functions and initial settings
    def cache_data(self):
        # Load config file as json
        with open(settings.config_path, "r") as config_file:
            json_data = json.loads(config_file.read())

        # For administrative commands
        self.whitelist = json_data["whitelist"]
        # Users in this dict can't use n!play
        self.play_blacklist = json_data["play_blacklist"]
        # This whitelist is for the n!am command. Be careful.
        self.am_whitelist = json_data["am_whitelist"]
        # If a guild and user are in this blacklist, debug_print will ignore it
        self.message_log_blacklist = json_data["message_log_blacklist"]
        # For the autoreaction feature
        self.autoreact_list = json_data["autoreact_list"]

