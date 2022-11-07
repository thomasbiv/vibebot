# vibebot
*Discord music/party bot.*

Vibe Bot is a simple and easy-to-use Discord bot created for the purpose of music and various other functionalities.
This is a personal project of mine that I constantly am updating/fixing, so I hope you enjoy using it!

### NOTE:

The following instructions are with Windows machines in mind, but the process is mostly consistant across all systems. For installation commands specific to your operating system, please visit the documentation links that will be provided in the instructions below.

## Setup and Installation

In order to set Vibe Bot up locally, you must have the latest version of Python3 installed. The latest stable build of FFmpeg must also be installed. Both of these downloads can be found here:
* [Python3](https://www.python.org/downloads/)
* [FFmpeg](https://www.ffmpeg.org/download.html#build-windows)

Also, be sure you are downloading the correct version of FFmpeg that coincides with your operating system. The different packages can be selected from the link provided above.

FFmpeg should download as a zipped folder. Once downloaded, extract the files and rename the new file to just ```ffmpeg```. Next, copy this file and paste it into your C drive.

Now that FFmpeg is downloaded, you will have to add it to PATH. To accomplish this, go to:

*Control Panel > System and Security > System > Advanced System Settings > Environment Variables > Path (Double Click)*

Now, add FFmpeg to PATH by selecting 'New' and typing the location of your FFmpeg file:

```
C:\ffmpeg\bin
```
To ensure that FFmpeg was installed correctly, access your command window by typing ```cmd``` in the Windows search bar. In the command window, enter this line:

```
ffmpeg -version
```

If software and build information appears on the command window, FFmpeg was successfully installed. If the command window returns that FFmpeg was not installed correctly, it is recommended that your computer is restarted, and the FFmpeg version is checked again.

### Libraries

Once Python3 is installed, the proper libraries to run the bot must be installed as well. For the next few installs, open your command window by again typing ```cmd``` in the Windows search bar. 

First, you'll need to pick up discord.py. Type or copy/paste this line into the command window:

```
pip install discord.py
```

For a more customized experience or for additional help, the full discord.py documentation can be found [here.](https://discordpy.readthedocs.io/en/stable/)

Second, youtube-dl will need to be installed. Type or copy/paste this line into the command window:

```
-m pip install -U youtube_dl
```

For a more customized experience or for additional help, the full youtube_dl documentation can be found [here.](https://youtube-dl.readthedocs.io/en/latest/)

Third, dotenv will need to be installed. Type or copy/paste this line into the command window:

```
pip install python-dotenv
```

For a more customized experience or for additional help, the full dotenv documentation can be found [here.](https://pypi.org/project/python-dotenv/)

Fourth, PyNaCl will need to be installed. Type or copy/paste this line into the command window:

```
pip install PyNaCl
```

For a more customized experience or for additional help, the full PyNaCl documentation can be found [here.](https://pynacl.readthedocs.io/en/latest/install/)

## Tokens

After all required libraries are installed, the connection between your discord bot and the code can be made. All discord bots have a special token that allows developers to access them. This token is extremely important and should only be seen by you.

### IMPORTANT NOTE:

Do **NOT** upload your token to any website for any reason or give your token to anyone you do not trust with the utmost certainty. When someone has access to your token, they also have access to your bot which means it is possible for them to use your bot with malicious intent.

Before linking your bot, it is recommended that your bot is added to your server of choice first. To link your discord bot to the python code present here, open your preferred coding environment and replace the placeholder text next to 'DISCORD_TOKEN = ' with your unique token. Then, rename ```sample.env``` to simply ```.env```

After this has been completed, Vibe Bot should be fully operational. Run the bot, and type ```$help``` in discord text chat to view all available command information. Enjoy!

## Commands Summary

Below is a list of all the current commands with descriptions.

### Useful Functions

* help
  * Description: View information on all commands or on a specified command.
  * Syntax: ```$help``` or ```$help <command name>```
* roll
  * Description: Roll a die with the requested amount of sides.
  * Syntax: ```$roll <amount>```
* ping
  * Description: Display the latency of Vibe Bot.
  * Syntax: ```$ping```
* eightball
  * Description: Ask a question to the Magic 8 Ball and recieve your fortune...
  * Syntax: ```$eightball <question>```
* purge
  * Description: Purges (clears) the last specified amount of messages (Default = 5).
  * Syntax: ```$purge <amount>```
* poll
  * Description: Create a new poll.
  * Syntax: ```$poll <topic>```

### Audio Functions

* youtube
  * Description: Search for a YouTube video!
  * Syntax: ```$youtube <query>```
* join
  * Description: Have Vibe Bot join your voice channel.
  * Syntax: ```$join```
* leave
  * Description: Have Vibe Bot leave your voice channel.
  * Syntax: ```$leave```
* pause
  * Description: Pause the current selection being played in the voice channel.
  * Syntax: ```$pause```
* resume
  * Description: Resume the current selection that is paused in the voice channel.
  * Syntax: ```$resume```
* skipq
  * Description: Skip the specified amount of selections in the queue (Default = 1).
  * Syntax: ```$skipq <amount>```
* enq
  * Description: Add audio from YouTube to the queue.
  * Syntax: ```$enq <query or link>```
* delq
  * Description: Delete the specified selection in the queue.
  * Syntax: ```$delq <number>```
* viewq
  * Description: View the current selections in the queue (Default page number = 1).
  * Syntax: ```$viewq <queue page number>```
* clear
  * Description: Stop the current selection being played and clear the queue.
  * Syntax: ```$clear```
* play
  * Description: Play audio from YouTube using keywords or a url. Also adds to queue.
  * Syntax: ```$play <query or link>```
* playq
  * Description: Play the current queue.
  * Syntax: ```$playq```
* shuffleq
  * Description: Shuffle the current queue.
  * Syntax: ```$shuffleq```
* replay
  * Description: Restart the current selection from the beginning.
  * Syntax: ```$replay```
* playlist
  * Description: Play a playlist off of YouTube using a playlist url. Adds to queue.
  * Syntax: ```$playlist <youtube playlist link>```
* currsong
  * Description: View the name of the current selection.
  * Syntax: ```$currsong```
* moveto
  * Description: Move a selection to a different spot in the queue.
  * Syntax: ```$moveto <index of selection to move> <index to move selection to>```
* repeat
  * Description: Repeat the current selection a given amount of times (DEFAULT/MAX = 20).
  * Syntax: ```$repeat <num of repeats>```
* repeatnum
  * Description: View the remaining repetitions left on a selection.
  * Syntax: ```$repeatnum```
* lyrics
  * Description: Get the lyrics of a specified selection in the queue (DEFAULT = 0).
  * Syntax: ```$lyrics <queue location>```
* swapq
  * Description: Switch two selections in the queue.
  * Syntax: ```$swapq <index of first selection> <index of second selection>```
  
### NOTE:

Because Vibe Bot accesses YouTube with no account logged in, age-restricted videos cannot be played in voice chats. If Vibe Bot is queried to play a video with an age-restriction, the bot will join and immediately idle. An update is in the works to correct this by skipping the newly enqueued selection if the bot detects age-restricted content.


More commands are planned to be added soon! If you have any questions or suggestions feel free to message me on Twitter:

---------------------------

Thomas Bivins

[@thomasbiv](https://twitter.com/thomasbiv)

USF Computer Engineering

---------------------------
