# MAKBOT DISCORD

----------

## Commands

Please Note: All items that are not yet implemented have been placed below their corresponding tables.

#### General

| Command                 | Description                            |
| ------------------------| ---------------------------------------|
| `.join` / `.j`          | Adds Makbot to the current VC          | 
| `.disconnect` /`.dc`    | Disconnects Makbot.                    | 


#### Playback
| Command                 | Description                             |
| ------------------------| ----------------------------------------|
| `.p <Query/URL>` / `.play <Query/URL>`  | Plays a track from the URL provided or searches youtube and plays the first result for a given query.             | 
| `.pause`                | Pauses the currently playing track.     | 
| `.resume` / `.r`        | Resumes a paused track.                 | 

<pre>(add shorthand for pause?)</pre>


#### Queue Controls
| Command                 | Description                             |
| ------------------------| ----------------------------------------|
| `.queue` / `.q`         | Prints the queue.                       | 


#### Spotify
To be confirmed

## Known Issues

* Bot still sends message with pause/resume/stopping even if not playing; however, not an issue when bot is not in voice channel.

* There appears to sometimes be slight lag in audio stream, not sure why this happening. It is a rare occurrence.

* Volume can fluctuate a lot depending on audio source, perhaps could be set to a value in code.

* If songs requested while downloading other song, plays preferencially