[![CodeFactor](https://www.codefactor.io/repository/github/sclafus/twitch-chatbot-for-gosumemory/badge)](https://www.codefactor.io/repository/github/sclafus/twitch-chatbot-for-gosumemory)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Sclafus/twitch-chatbot-for-gosumemory/Pylint?style=flat)

A basic and lightweight Twitch chatbot to use with [gosumemory](https://github.com/l3lackShark/gosumemory)!
# Features
`!np` responds in chat with the currently playing map and a URL for the download link

`!skin` responds in chat with the skin currently in use with a URL to download it. The message is dinamically generated. New skins are automatically uploaded to [mega.nz](https://mega.nz). The URLs are automatically shortened using [tinyurl](https://tinyurl.com/)

`!owo` oωo
# Installation
- Download the [latest release](https://github.com/Sclafus/twitch-chatbot-for-gosumemory/releases/latest) for your operating system (coming soon...)

- Follow [Step 2](#step-2-create-a-new-twitch-app) and [Step 3](#step-3-create-config)

- Open your executable and enjoy
# Development Installation
As of today, `twitchio` has been forced to version 1.2.3 in `requirements.txt`. This is needed since `twitchio` version 2.0 is now out and I don't really have time to port the existing version to the new version at the moment. I might assume that `twitchio` 2.0 fixes the error with `websockets>=9.0`. I will fix everything soon™️. ETA: October 2021 (quite busy at the moment sorry lads).
## Step 1: clone the repository, install python and dependencies 
- Install [Python](https://www.python.org/) and add it to PATH

- Clone the repository - [Download zip](https://github.com/Sclafus/twitch-chatbot-for-gosumemory/archive/refs/heads/senpai.zip)

- Open a terminal and type:
```bash 
pip install -r requirements.txt
```
or 
```bash
pip3 install -r requirements.txt
```
to install the required libraries

## Step 2: create a new twitch app
- Login on [Twitch Developers](https://dev.twitch.tv/)
- Register a [new Twitch Application](https://dev.twitch.tv/console/apps). Choose a name (eg. "Osu Chatbot") and set your URL to `https://127.0.0.1`. The category should be "Chat Bot".
- Copy the `Client ID`, it will be needed in [Step 3](#step-3-create-config)

- Open your browser in incognito mode and visit [twitchapps](https://twitchapps.com/tmi/) to get your oauth token. You will need to login with your bot account, not your main account.
- Copy the oauth token

## Step 3: create config
- Create a `config.txt` file with the following content:

```bash
# Twitch config
TMI_TOKEN = ####################               # starts with "oauth:"
CLIENT_ID = ##################
BOT_NICK = your_chatbot_username
BOT_PREFIX = !
CHANNEL = your_channel_username
GOSUMEMORY_JSON_URL = http://127.0.0.1:24050/json # probably this

# Mega config
MEGA_EMAIL = example@email.com
MEGA_PASSWORD = yourpassword                   # not very secure, I know...
                                               # also 2FA is not supported
MEGA_FOLDER = folder/subfolder
```

## Step 4: play more
- Execute `python twitch_chatbot.py` in the terminal or simply double click it

# Bug Reports

Feel free to open an Issue for new features, unexpected behaviors or anything else really!

If you don't want to open an Issue, you can [DM me on Discord](https://discordapp.com/users/108501885849202688), but please use issues since it's way more organized than my Discord DMs lol

# Contributions
We are very open to contribution and constructive criticism!

If you want to contribute to this project in any way, make a fork and make a pull request!

# Special Thanks to:
- [Gr3g0](https://github.com/Gr3g027) for the skin command


# Todos sorted by priority
- Switch to twitchio 2.0
- Automatic builds on commit using pyinstaller
- Add mikuia-like functionality
- Handle missing MEGA_FOLDER (defaulting to root folder)
