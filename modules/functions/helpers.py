import time, os
from dotenv import load_dotenv

import settings

# ---------------------------------------------------------------
# Print to terminal and to log

def debug_print(text):
    print(text)
    if settings.write_to_log:
        with open(settings.discord_log_path, "a") as discord_log:
            if text.strip() != "":
                discord_log.write(text + "\n")

# ---------------------------------------------------------------
# Printing errors to bot_error_path

def error_print(text):
    print("----------------------------------")
    print(text)
    print("----------------------------------")
    if settings.write_to_error_log:
        now = time.strftime("%d %b %Y - %H:%M:%S") 
        with open(settings.discord_log_path, "a") as discord_log:
            discord_log.write(f"[Bot] [ET] {now}\n")
        with open(settings.bot_error_path, "a") as error_log:
            error_log.write(f"=======================\n{now}\n{str(text)}\n=======================\n")

# ---------------------------------------------------------------
# Backup config file

def bak_config_file(file_path):
    try:
        with open(file_path, "r") as ifile:
            output_file = file_path + ".bak"
            with open(output_file, "w") as ofile:
                ofile.write(ifile.read())
    except Exception as e:
        error_print(e)

# ---------------------------------------------------------------
# Check default files

def check_defaults():
    # config/config.json
    if not os.path.isfile("config/config.json"):                # The default config does not exist by default
        print("I can't find config/config.json")
        print("If this is your first time running the program, you can use the default one as a template.")
        if os.path.isfile("config/config.json.default"):        # Only ask to clone if there is a file to clone
            try:
                clone_input = input("Do you want me to copy the template to the config.json file? (Yes/No): ")
            except KeyboardInterrupt:
                print("\nNot copying...")
                exit(1)
            if "y" in clone_input.lower():
                with open("config/config.json.default", "r") as default_file:
                    with open("config/config.json", "w") as config_file:
                        for line in default_file:
                            config_file.write(line)
                print("Successfully copied config/config.json\n")
            else:
                print("Not copying...")
                exit(1)
        else:
            print("Exiting...")
            exit(1)

    #.env
    if not os.path.isfile(".env"):
        print("I can't find .env")
        print("If this is your first time running the program, you can use the default one as a template.")
        if os.path.isfile(".env_default"):
            try:
                clone_input = input("Do you want me to copy the template to the .env file? (Yes/No): ")
            except KeyboardInterrupt:
                print("\nNot copying...")
                exit(1)
            if "y" in clone_input.lower():
                with open(".env_default", "r") as default_file:
                    with open(".env", "w") as config_file:
                        for line in default_file:
                            config_file.write(line)
                print("Successfully copied .env\n")
            else:
                print("Not copying...")
                exit(1)
        else:
            print("Exiting...")
            exit(1)

# ---------------------------------------------------------------
# Check default token from .env

def get_env_token():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    if token[1:-1] == "YOUR_TOKEN_HERE":
        print("Detected default token")
        print("You need to edit the TOKEN (in the .env file) before starting the bot!")
        exit(1)
    elif token[1:-1] == "DOCKER_TOKEN":
        print("Docker token detected.")
        while True:
            user_token = raw_input("Please input your token: ")
            if len(user_token) != 59:
                print("\rWrong token length. Please try again...")
                continue
            else:
                print("\rDone.")
                break
    else:
        return token
