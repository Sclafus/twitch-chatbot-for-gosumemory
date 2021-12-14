from twitchio.ext import commands


from outputs.outputs import Outputs
from bot.osu_specific import Osu
from data.gosumemory import data


class Bot(commands.Bot):

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
        if message.echo: return
        self.outputs.print_message(author=message.author.name, message=message.content)

        await self.handle_commands(message)

    # async def event_error(error, data):
    #     outputs.print_error(data)

    @commands.command()
    async def np(self, ctx: commands.Context):
        metadata = data.get_map()
        await ctx.send(f'{self.outputs.string_map(metadata=metadata)}')

    @commands.command()
    async def skin(self, ctx: commands.Context):
        await ctx.send("la mia skin epica owo")

    @commands.command()
    async def owo(self, ctx: commands.Context):
        await ctx.send(f"/me OωO @{ctx.author.name}")
