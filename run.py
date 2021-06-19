import requests
import os

import colorama

from time import sleep
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env'))
TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CHANNEL = os.environ.get('CHANNEL')
GOSUMEMORY_JSON = os.environ.get('GOSUMEMORY_JSON_URL')

# Colors
colorama.init(autoreset=True)
RED = "\033[1;31;40m"
GREEN = "\033[1;32;40m"
CYAN = "\033[1;34;40m"

def get_map() -> dict:
    '''Gets data from gosumemory, returns current beatmap information'''
    try:
        # get data from gosumemory
        api_data = requests.get(GOSUMEMORY_JSON).json()
        if 'error' not in api_data:
            # download link
            beatmap_id = api_data['menu']['bm']['id']
            beatmap_url = f"https://osu.ppy.sh/b/{beatmap_id}"

            # beatmap metadata
            beatmap_metadata = api_data['menu']['bm']['metadata']

            return {
                "url": beatmap_url,
                "title": beatmap_metadata['title'],
                "artist": beatmap_metadata['artist'],
                "diff": beatmap_metadata['difficulty'],
                "mapper": beatmap_metadata['mapper']
            }

        print(f"{RED}osu is not running!")
        return None

    except requests.exceptions.ConnectionError:
        # error handling, can't connect to gosumemory
        print(f"{RED}Could not connect to gosumemory socket!")
        return None

def get_skin() -> dict:
    '''Gets data from gosumemory, returns current skin title'''
    try:
        # get data from gosumemory
        api_data = requests.get(GOSUMEMORY_JSON).json()
        if 'error' not in api_data:
            # skin
            skin_name = api_data['settings']['folders']['skin']

            return {
                "skin": skin_name
            }
        print(f"{RED}osu is not running!")
        return None

    except requests.exceptions.ConnectionError:
        # error handling, can't connect to gosumemory
        print(f"{RED}Could not connect to gosumemory socket!")
        return None


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)


@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{GREEN}{BOT_NICK.upper()} is online!")


@bot.event
async def event_message(ctx):
    chat_msg = f"{ctx.author.name.upper()}: {ctx.content}"
    if ctx.author.name.lower() == BOT_NICK.lower():
        print(f"{GREEN}{chat_msg}")
    else: 
        print(f"{chat_msg}")
    await bot.handle_commands(ctx)


@bot.command(name='np', aliases=['nowplaying','song'])
async def now_playing(ctx):
    metadata = get_map()
    if metadata:
        await ctx.send(f"/me {metadata['artist']} - {metadata['title']} [{metadata['diff']}] by {metadata['mapper']} {metadata['url']}")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")

@bot.command(name='skin')
async def skin(ctx):
    skin = get_skin()
    if skin:
        skin_s = " ".join(skin['skin'].split())
        await ctx.send(f"/me Right now {CHANNEL} is using {skin_s}")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")

@bot.command(name='owo')
async def owo(ctx):
    await ctx.send(f"/me OwO @{ctx.author.name}")

if __name__ == '__main__':
    bot.run()
