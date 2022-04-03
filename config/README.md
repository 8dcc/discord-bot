# Configuration file

The configuration file defines some checks the bot will do.  
The bot currently reads all the whitelists and blacklists from the configuration file

### Whitelist
For administrative commands.  
**Structure:**
```json
{
    "whitelist": {
        "111111111111111111": [
            "123213123123123123",
            "123213213213123123"
        ],
        "213123123123123123": [
            "123213123123123123",
            "123213213213123123"
        ]
    }
}
```

### AM whitelist
This whitelist is for the `n!am` command. Be careful.  
**Structure:**
```json
{
    "am_whitelist": [
        "123213123123123123",
        "223232323232312323"
    ]
}
```

### Play blacklist
Users in this dict can't use `n!play`.  
**Structure:**
```json
{
    "play_blacklist": {
        "111111111111111111": [
            "123123213123123123",
            "123123213123123123"
        ],
        "222222222222222222": [
            "123123123123123123",
            "123123123123123123"
        ]
    }
}
```

### Message log blacklist
If a guild and user are in this whitelist, the message logging will be ignored.  
**Structure:**
```json
{
    "message_log_blacklist": {
        "111111111111111111": [
            "123123123123123123",
            "123123123123123123"
        ],
        "222222222222222222": [
            "212121212312112122",
            "123123123123123123"
        ]
    }
}
```

### Autoreact
You can find the emoji list [here](https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias).  
**Structure:**
```json
{
    "autoreact_list": {
        "GUILD_ID_111111111" {
            "USER_ID_1212121212": [
                ":EMOTE_LIST:",
                ":duck:",
                "..."
            ]
        }
    }
}
```
