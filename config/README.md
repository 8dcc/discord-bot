# Configuration file

The configuration file defines some checkins the bot will do.  
Currently check the autoreact feature.  


### Autoreact
You can find the emoji list [here](https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias).  
Structure:
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
