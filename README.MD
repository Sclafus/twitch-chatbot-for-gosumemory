[![CodeFactor](https://www.codefactor.io/repository/github/sclafus/twitch-chatbot-for-gosumemory/badge)](https://www.codefactor.io/repository/github/sclafus/twitch-chatbot-for-gosumemory)

# Installation

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
- Copy the `Client ID`, it will be needed in [Step 3](#step-3-create-env)

- Open your browser in incognito mode and visit [twitchapps](https://twitchapps.com/tmi/) to get your oauth token. You will need to login with your bot account, not your main account.
- Copy the oauth token

## Step 3: create .env
- Create a .env file with the following content:

```bash
TMI_TOKEN = ####################    #starts with "oauth:"
CLIENT_ID = ##################
BOT_NICK = your_chatbot_username
BOT_PREFIX = !
CHANNEL = your_channel_username
GOSUMEMORY_JSON_URL = http://127.0.0.1:24050/json #probably this
```

## Step 4: play more
- Execute `python twitch_chatbot.py` in the terminal or simply double click it

# Contributions
We are very open to contribution and constructive criticism! 


Feel free to open an Issue for new features, unexpected behaviors or anything else really!


If you don't want to open an Issue, you can [DM me on Discord](https://discordapp.com/users/108501885849202688), but please use issues since it's way more organized than my Discord DMs lol