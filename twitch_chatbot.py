'''
Main program
'''

import sys
from twitchio.ext import commands
from utils import data, colors
twitch_data = data.get_twitch_data()

# checking env
if [True for match in twitch_data.values() if match in ['', None]]:
    print(f"""{colors.RED}Your .env is missing Twitch values.
     The program will not work without them.""")
    sys.exit()


bot = commands.Bot(
    irc_token=twitch_data['TMI_TOKEN'],
    client_id=twitch_data['CLIENT_ID'],
    nick=twitch_data['BOT_NICK'],
    prefix=twitch_data['BOT_PREFIX'],
    initial_channels=[twitch_data['CHANNEL']]
)


@bot.event
async def event_ready():
    ''' Runs once the bot has established a connection with Twitch '''

    print(f"{colors.CYAN}{twitch_data['BOT_NICK']} is online!")


@bot.event
async def event_message(ctx):
    ''' Runs once every time a new message appears in chat '''

    if ctx.author.name.lower() == twitch_data['BOT_NICK'].lower():
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.GREEN}{ctx.content}"
    else:
        chat_msg = f"{colors.LIGHT_PURPLE}{ctx.author.name}: {colors.NOCOLOR}{ctx.content}"
    print(chat_msg)
    await bot.handle_commands(ctx)


@bot.command(name='np', aliases=['nowplaying', 'song'])
async def now_playing(ctx):
    ''' Sends the currently playing map and URL in chat '''

    metadata = data.get_map()
    if metadata:
        await ctx.send(f"""/me {metadata['artist']} - {metadata['title']}
         [{metadata['diff']}] by {metadata['mapper']} {metadata['url']}""")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='skin')
async def skin(ctx):
    ''' Sends the currently used skin and URL in chat '''

    skin_dict = data.get_skin()
    if skin_dict:
        # removing leading and trailing whitespaces
        skin_stripped = " ".join(skin_dict['skin'].split())

        if skin_dict['url']:
            await ctx.send(f"""/me Right now {twitch_data['CHANNEL']}
            is using {skin_stripped} | Link: {skin_dict['url']}""")
        else:
            await ctx.send(f"""/me Right now {twitch_data['CHANNEL']}
            is using {skin_stripped} | No URL for you!""")
    else:
        await ctx.send("/me Sorry bud, can't help you with that")


@bot.command(name='owo')
async def owo(ctx):
    ''' Sends an OωO in chat '''
    await ctx.send(f"/me OωO @{ctx.author.name}")


if __name__ == '__main__':
    bot.run()
