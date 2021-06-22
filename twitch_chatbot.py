from twitchio.ext import commands
from utils import data, colors
from skin_uploader import get_skin_url

twitch_data = data.get_twitch_data()

# checking env
if [True for match in twitch_data.values() if match in ['', None]]:
    print(f"{colors.RED}Your .env is missing Twitch values. The program will not work without them.")
    exit()


bot = commands.Bot(
    irc_token = twitch_data['TMI_TOKEN'],
    client_id = twitch_data['CLIENT_ID'],
    nick = twitch_data['BOT_NICK'],
    prefix = twitch_data['BOT_PREFIX'],
    initial_channels = [twitch_data['CHANNEL']]
)


@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{colors.CYAN}{twitch_data['BOT_NICK']} is online!")


@bot.event
async def event_message(ctx):

    if ctx.author.name.lower() == twitch_data['BOT_NICK'].lower():
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.GREEN}{ctx.content}"
    else:
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.NOCOLOR}{ctx.content}"
    print(chat_msg)
    await bot.handle_commands(ctx)


@bot.command(name='np', aliases=['nowplaying', 'song'])
async def now_playing(ctx):
    metadata = data.get_map()
    if metadata:
        await ctx.send(f"/me {metadata['artist']} - {metadata['title']} [{metadata['diff']}] by {metadata['mapper']} {metadata['url']}")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='skin')
async def skin(ctx):
    skin = data.get_skin()
    if skin:
        # removing leading and trailing whitespaces
        skin_stripped = " ".join(skin['skin'].split())
        if skin['url']:
            await ctx.send(f"Right now {twitch_data['CHANNEL']} is using {skin_stripped} | Link: {skin['url']}")
        else:
            await ctx.send(f"Right now {twitch_data['CHANNEL']} is using {skin_stripped} | No URL for you!")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='owo')
async def owo(ctx):
    await ctx.send(f"/me OωO @{ctx.author.name}")


if __name__ == '__main__':
    bot.run()
