from os import environ
from dotenv import load_dotenv


class Config:
    def __init__(self, filename: str = "config.txt"):
        load_dotenv(filename)

        self.TMI_TOKEN = environ.get("TMI_TOKEN")
        self.CLIENT_ID = environ.get("CLIENT_ID")
        self.BOT_NICK = environ.get("BOT_NICK")
        self.BOT_PREFIX = environ.get("BOT_PREFIX")
        self.CHANNEL = environ.get("CHANNEL")
        self.GOSUMEMORY_JSON = environ.get("GOSUMEMORY_JSON_URL")
        self.MEGA_EMAIL = environ.get("MEGA_EMAIL")
        self.MEGA_PASSWORD = environ.get("MEGA_PASSWORD")
        self.MEGA_FOLDER = environ.get("MEGA_FOLDER")

    def get_mega_data(self) -> dict:
        """Returns mega config data."""

        return {
            "MEGA_EMAIL": self.MEGA_EMAIL,
            "MEGA_PASSWORD": self.MEGA_PASSWORD,
            "MEGA_FOLDER": self.MEGA_FOLDER,
        }

    def get_twitch_data(self) -> dict:
        """Returns twitch config data."""

        return {
            "TMI_TOKEN": self.TMI_TOKEN,
            "CLIENT_ID": self.CLIENT_ID,
            "BOT_NICK": self.BOT_NICK,
            "BOT_PREFIX": self.BOT_PREFIX,
            "CHANNEL": self.CHANNEL,
        }

    def is_config_usable(self) -> bool:
        """Checks if values are valid"""
        return self.is_twitch_config_valid() and self.GOSUMEMORY_JSON is not None

    def is_twitch_config_valid(self) -> bool:
        """Checks if the twitch values are valid"""
        return all(value is not None for value in self.get_twitch_data().values())

    def is_mega_config_valid(self) -> bool:
        """Checks if the mega values are valid"""
        return all(value is not None for value in self.get_mega_data().values())
