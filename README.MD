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
- TODO mini tutorial on how to create a twitch app


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
- Execute `python twitch_chatbot.py` in the terminal (CMD, powershell, xterm, whatever) or simply double click it
