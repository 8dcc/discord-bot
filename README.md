# Discord bot
**My discord bot made in python.**
## Features
### Music:
* `n!help` - shows a help similar to this readme.
* `n!play <url>` - Play audio in a voice channel.
* `n!join` - Join the user's channel.
* `n!join_channel <channel_name>` - Join the specified channel.
* `n!leave` - Leaves the current channel.
* `n!pause` - Pauses the audio.
* `n!resume` - Resumes the audio.
* `n!stop` - Stops the audio without leaving the channel.
### Administration:
This commands will only work if you are the bot owner or if you are in the whitelist.
* `n!kick @someone` to kick a user.
* `n!ban @someone` to ban a user.
* `n!move @someone <channel>` to move a user.
* `n!mute @someone` to mute a user. Also `n!m`.
* `n!unmute @someone` to unmute a user. Also `n!um`.
* `n!deafen @someone` to deafen a user. Also `n!d`.
* `n!undeafen @someone` to undeafen a user. Also `n!ud`.
* `n!purge @someone <messages_to_check>` will check X messages, and will delete them if the author is the specified user. Also `n!clean`.

This commands will only work if you are the bot owner:
* `n!selfadmin` to give admin to the bot owner. (Will create a role named 'BOT' with all the permissions)
### Misc:
* `ping` to make sure it works
* Detects if a message contains `uwu`, then screams.
## Todo
- [X] Bot needs to be on a channel to play music, if you use `n!play <song>` the bot will join, but you will need to type the command again for it to work. You can use `n!join` to make the bot join the channel before using `n!play`.
- [X] Add a `n!help` command.
- [ ] Wanna play blackjack with the bot.
