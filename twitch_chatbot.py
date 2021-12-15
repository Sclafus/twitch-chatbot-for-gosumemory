'''
Main program
'''
from bot.bot import Bot
from data.config import Config

if __name__ == '__main__':
    config = Config()
    bot = Bot(access_token=config.get_twitch_data()[
              'TMI_TOKEN'], prefix='!', channels=[config.get_twitch_data()['CHANNEL']])
    bot.run()
