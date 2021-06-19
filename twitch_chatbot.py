import requests
import os

import colorama

from time import sleep
from twitchio.ext import commands
from dotenv import load_dotenv

# colors
colorama.init(autoreset=True)
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
NOCOLOR = "\033[0m"
LIGHT_PURPLE = "\033[95m"

# loading env
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env'))
env = {
    "TMI_TOKEN": os.environ.get('TMI_TOKEN'),
    "CLIENT_ID": os.environ.get('CLIENT_ID'),
    "BOT_NICK": os.environ.get('BOT_NICK'),
    "BOT_PREFIX": os.environ.get('BOT_PREFIX'),
    "CHANNEL": os.environ.get('CHANNEL'),
    "GOSUMEMORY_JSON": os.environ.get('GOSUMEMORY_JSON_URL')
}
# checking env
if [True for match in env.values() if match in ['', None]]:
    print(f"{RED}Your .env is not valid or missing.")
    exit()


def get_data() -> dict:
    try:
        # get data from gosumemory
        api_data = requests.get(env['GOSUMEMORY_JSON']).json()
        return api_data if 'error' not in api_data else None

    except requests.exceptions.ConnectionError:
        # error handling, can't connect to gosumemory
        print(f"{RED}Could not connect to gosumemory socket!")
        return None


def get_map() -> dict:
    '''Gets data from gosumemory, returns current beatmap informations'''

    api_data = get_data()
    if api_data:
        # download link
        beatmap_id = api_data['menu']['bm']['id']
        beatmap_url = f"https://osu.ppy.sh/b/{beatmap_id}"

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


def get_skin() -> dict:
    '''Gets data from gosumemory, returns skin informations'''

    api_data = get_data()
    if api_data:

        skin_name = api_data['settings']['folders']['skin']
        return {
            "skin": skin_name,
            "url": None
        }

    print(f"{RED}osu is not running!")
    return None


bot = commands.Bot(
    irc_token=env['TMI_TOKEN'],
    client_id=env['CLIENT_ID'],
    nick=env['BOT_NICK'],
    prefix=env['BOT_PREFIX'],
    initial_channels=[env['CHANNEL']]
)


@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{CYAN}{env['BOT_NICK']} is online!")


@bot.event
async def event_message(ctx):

    if ctx.author.name.lower() == env['BOT_NICK'].lower():
        chat_msg = f"{LIGHT_PURPLE}{ctx.author.name}: {GREEN}{ctx.content}"
    else:
        chat_msg = f"{LIGHT_PURPLE}{ctx.author.name}: {NOCOLOR}{ctx.content}"
    print(chat_msg)
    await bot.handle_commands(ctx)


@bot.command(name='np', aliases=['nowplaying', 'song'])
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
        # removing leading and trailing whitespaces
        skin_stripped = " ".join(skin['skin'].split())
        await ctx.send(f"/me Right now {env['CHANNEL']} is using {skin_stripped}")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='owo')
async def owo(ctx):
    await ctx.send(f"/me OωO @{ctx.author.name}")

if __name__ == '__main__':
    bot.run()
