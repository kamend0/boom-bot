# boom-bot Discord bot

A simple Discord bot with two jobs:

* Play noises (mp3 files in the same directory as main.py) when someone enters chat, or on command (!!play clip).
* Announce who enters chat by their Discord name, or by a specified alias.

!!toggleUseful will switch behavior from playing a random mp3 file when someone joins to saying who joined using Google's Text to Speech API. If they don't have an alias specified in aliases.py (a lookup dictionary), their Discord display name will be used - not their server nickname.

Please read through main.py for all commands. They include: join, leave, play, toggleUseful, isUseful.

Uploading for convenience and as a jumping-off point for future projects.