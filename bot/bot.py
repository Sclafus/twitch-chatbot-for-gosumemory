'''Bot module'''
from twitchio.ext import commands

# pylint: disable=import-error, no-name-in-module
from bot.osu_specific import Osu
from outputs.outputs import Outputs
from data.gosumemory import gosumemory


class Bot(commands.Bot):
    '''Bot class, handles all the bot logic'''

    def __init__(self, access_token='', prefix='', channels=None):
        '''Bot class constructor'''

        self.osu = Osu()
        self.outputs = Outputs()
        super().__init__(token=access_token, prefix=prefix,
                         initial_channels=[] if channels is None else channels)

    async def event_ready(self):
        ''' Runs once the bot has established a connection with Twitch. '''
        self.outputs.print_info(f'Logged in as {self.nick}')

    async def event_message(self, message):
        '''Runs every time a new message is received'''
        # if osu.is_map_request(message.content):
        #     outputs.print_map_request(author=message.author.name, message=message.content)
        # else:
        if message.echo:
            return
        self.outputs.print_message(message.author.name, message.content)

        await self.handle_commands(message)

    # async def event_error(error, data):
    #     outputs.print_error(data)

    # pylint: disable=invalid-name
    @commands.command()
    async def np(self, ctx: commands.Context):
        '''Now playing command'''
        metadata = gosumemory.get_map()
        if metadata:
            await ctx.send(f'{self.outputs.string_map(metadata=metadata)}')
        else:
            Outputs.print_error("Could not connect to gosumemory socket!")
            await ctx.send('Could not connect to gosumemory, sorry!')

    @commands.command()
    async def skin(self, ctx: commands.Context):
        '''Skin command'''
        skin = gosumemory.get_skin()
        if skin:
            await ctx.send(f"{skin['skin']} {skin['url']}")
        else:
            Outputs.print_error("Could not connect to gosumemory socket!")
            await ctx.send('Could not connect to gosumemory, sorry!')

    @commands.command()
    async def owo(self, ctx: commands.Context):
        '''OwO command'''
        await ctx.send(f"/me OωO @{ctx.author.name}")
