# vibebot
*Discord music/party bot.*

Vibe Bot is a simple and easy-to-use Discord bot created for the purpose of music amd various other functionalities.
This is a personal project of mine that I constantly am updating, so I hope you enjoy using it!

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

## Keys

After all required libraries are installed, the connection between your discord bot and the code can be made. All discord bots have a special key that allows developers to access them. This key is extremely important and should only be seen by you.

### IMPORTANT NOTE:

Do **NOT** upload your key to any website for any reason or give your key to anyone you do not trust with the utmost certainty. When someone has access to your key, they also have access to your bot which means it is possible for them to use your bot with malicious intent.

Before linking your bot, it is recommended that your bot is added to your server of choice first. To link your discord bot to the python code present here, open your preferred coding environment and replace the placeholder text next to 'DISCORD_TOKEN = ' with your unique key. Then, rename ```sample.env``` to simply ```.env```

After this has been completed, Vibe Bot should be fully operational. Run the bot, and type ```$help``` in discord text chat to view all available command information. Enjoy!


Thomas Bivins

USF Computer Engineering

