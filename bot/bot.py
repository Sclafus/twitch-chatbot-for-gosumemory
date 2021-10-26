from twitchio.ext import commands

from outputs import Outputs
from osu_specific import Osu
from data import data

osu = Osu()
outputs = Outputs()

class Bot(commands.Bot):

    def __init__(self, access_token='', prefix='', channels=[]):
        '''Bot class constructor'''
        super().__init__(token=access_token, prefix=prefix, initial_channels=channels)

    async def event_ready(self):
        ''' Runs once the bot has established a connection with Twitch. '''
        outputs.print_warning(f'Logged in as {self.nick}')

    async def event_message(self, message):
        '''Runs every time a new message is received'''
        # if osu.is_map_request(message.content):
        #     outputs.print_map_request(author=message.author.name, message=message.content)
        # else:
        import json 
        print(json.dumps(message.raw_data))
        outputs.print_message(author=message.author.name, message=message.content)

        await self.handle_commands(message)

    # async def event_error(error, data):
    #     outputs.print_error(data)

    @commands.command()
    async def np(self, ctx: commands.Context):
        metadata = data.get_map()
        await ctx.send(f'{outputs.string_map(metadata=metadata)}')

    @commands.command()
    async def skin(self, ctx: commands.Context):
        await ctx.send(f"la mia skin epica owo")

    @commands.command()
    async def owo(self, ctx: commands.Context):
        await ctx.send(f"/me OωO @{ctx.author.name}")

if __name__ == '__main__':
    bot = Bot(access_token=data.get_twitch_data()['TMI_TOKEN'], prefix='!', channels=['scla'])
    bot.run()