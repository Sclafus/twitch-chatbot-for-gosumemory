"""
Main program
"""
import sys

from bot.bot import Bot
from data.config import Config
from outputs.outputs import Outputs

if __name__ == "__main__":
    config = Config()

    if not config.is_config_usable():
        Outputs.print_error("Missing twitch information, exiting...")
        sys.exit(1)

    if not config.is_mega_config_valid():
        Outputs.print_warning(
            'Mega config is missing or invalid.\n'
            'You will not be able to upload automatically your skins.'
        )

    twitch_data = config.get_twitch_data()
    bot = Bot(
        access_token=twitch_data.tmi_token,
        prefix=twitch_data.bot_prefix,
        channels=[twitch_data.channel],
    )
    bot.run()
