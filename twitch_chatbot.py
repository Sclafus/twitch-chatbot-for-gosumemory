from twitchio.ext import commands
from utils import twitch_chatbot_env, colors, get_data
from skin_uploader import upload_skin


# checking env
if [True for match in twitch_chatbot_env.values() if match in ['', None]]:
    print(f"{colors.RED}Your .env is not valid or missing.")
    exit()


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

    print(f"{colors.RED}osu is not running!")
    return None


def get_skin() -> dict:
    '''Gets data from gosumemory, returns skin informations'''

    api_data = get_data()
    if api_data:

        skin_name = api_data['settings']['folders']['skin']
        skin_url = upload_skin()

        return {
            "skin": skin_name,
            "url": skin_url
        }

    print(f"{colors.RED}osu is not running!")
    return None


bot = commands.Bot(
    irc_token = twitch_chatbot_env['TMI_TOKEN'],
    client_id = twitch_chatbot_env['CLIENT_ID'],
    nick = twitch_chatbot_env['BOT_NICK'],
    prefix = twitch_chatbot_env['BOT_PREFIX'],
    initial_channels = [twitch_chatbot_env['CHANNEL']]
)


@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{colors.CYAN}{twitch_chatbot_env['BOT_NICK']} is online!")


@bot.event
async def event_message(ctx):

    if ctx.author.name.lower() == twitch_chatbot_env['BOT_NICK'].lower():
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.GREEN}{ctx.content}"
    else:
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.NOCOLOR}{ctx.content}"
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
        
        # TODO find a way to shorten the skin url
        await ctx.send(f"Right now {twitch_chatbot_env['CHANNEL']} is using {skin_stripped} | Link: {skin['url']}")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='owo')
async def owo(ctx):
    await ctx.send(f"/me OωO @{ctx.author.name}")

if __name__ == '__main__':
    bot.run()
