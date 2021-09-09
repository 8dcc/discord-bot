# Discord bot
**My discord bot made in python.**
## Features
### Music:
* `n!play <url>` - Play audio in a voice channel. (The bot needs to be in the channel, see Todo)
* `n!join` - Join the user's channel.
* `n!join_channel <channel_name>` - Join the specified channel.
* `n!leave` - Leaves the current channel.
* `n!pause` - Pauses the audio.
* `n!resume` - Resumes the audio.
* `n!stop` - Stops the audio without leaving the channel.
### Administration:
* `n!kick @someone` to kick a user (only works if you are the bot owner)
* `n!ban @someone` to ban a user (only works if you are the bot owner)
### Misc:
* `ping` to make sure it works
* Detects if a message contains `uwu`, then screams.
## Todo
* Bot needs to be on a channel to play music, if you use `n!play <song>` the bot will join, but you will need to type the command again for it to work. You can use `n!join` to make the bot join the channel before using `n!play`.
