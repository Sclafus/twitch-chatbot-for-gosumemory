'''
Main program
'''
from bot.bot import Bot
from data.gosumemory import data

if __name__ == '__main__':
    bot = Bot(access_token=data.get_twitch_data()[
              'TMI_TOKEN'], prefix='!', channels=[data.get_twitch_data()['CHANNEL']])
    bot.run()
