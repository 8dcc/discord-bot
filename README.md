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
* `n!selfadmin` to give admin to the bot owner (Will create a role named 'BOT' with all the permissions). Also `n!am`.
### Misc:
* `ping` to make sure it works
* Detects if a message contains `uwu`, then screams.
## Todo
- [X] Bot needs to be on a channel to play music, if you use `n!play <song>` the bot will join, but you will need to type the command again for it to work. You can use `n!join` to make the bot join the channel before using `n!play`.
- [X] Add a `n!help` command.
- [ ] Wanna play blackjack with the bot  **:^)**

## Related gists
* [discord_purge.py](https://gist.github.com/r4v10l1/a21360c3f92266c0b03db7cc9b73e7ff) - Discord bot purge 1.
* [discord_purge2.py](https://gist.github.com/r4v10l1/c684325e461d70c06b76277aedfe08d8) - Discord bot purge 2.
* [discord_purge3.py](https://gist.github.com/r4v10l1/c6af5d4149c0d6c04d4b8f94887a2ae3) - Discord bot purge 3.
* [check_inactive.py](https://gist.github.com/r4v10l1/0793c5e2d37bf77d5f279643f03d6112) - Check if the bot is alone in a channel for X secconds.
