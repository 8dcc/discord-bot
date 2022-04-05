import time

import settings

def debug_print(text):
    print(text)
    if settings.write_to_log:
        with open(settings.discord_log_path, "a") as discord_log:
            if text.strip() != "":
                discord_log.write(text + "\n")

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

def bak_config_file(file_path):
    try:
        with open(file_path, "r") as ifile:
            output_file = file_path + ".bak"
            with open(output_file, "w") as ofile:
                ofile.write(ifile.read())
    except Exception as e:
        error_print(e)

