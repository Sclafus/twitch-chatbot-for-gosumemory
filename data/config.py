'''Config file handler'''
from os import environ
from dataclasses import dataclass, fields
from dotenv import load_dotenv


@dataclass
class MegaConfig:
    '''Mega config class, stores the credentials for mega'''

    email: str
    password: str
    folder: str


@dataclass
class TwitchConfig:
    '''Twitch config class, stores the credentials for twitch'''

    tmi_token: str
    client_id: str
    bot_nick: str
    bot_prefix: str
    channel: str


class Config:
    '''Config class'''

    def __init__(self, filename: str = "config.txt"):
        load_dotenv(filename)
        self.twitch_config = TwitchConfig(
            tmi_token=environ.get("TMI_TOKEN"),
            client_id=environ.get("CLIENT_ID"),
            bot_nick=environ.get("BOT_NICK"),
            bot_prefix=environ.get("BOT_PREFIX"),
            channel=environ.get("CHANNEL"),
        )

        self.mega_config = MegaConfig(
            email=environ.get("MEGA_EMAIL"),
            password=environ.get("MEGA_PASSWORD"),
            folder=environ.get("MEGA_FOLDER"),
        )

        self.gosumemory_json = environ.get("GOSUMEMORY_JSON_URL")

    def get_mega_data(self) -> MegaConfig:
        """Returns mega config data."""
        return self.mega_config

    def get_twitch_data(self) -> TwitchConfig:
        """Returns twitch config data."""
        return self.twitch_config

    def get_gosumemory_url(self) -> str:
        """Returns the gosumemory url"""
        return self.gosumemory_json

    def is_config_usable(self) -> bool:
        """Checks if values are valid"""
        return self.is_twitch_config_valid() and self.gosumemory_json is not None

    def is_twitch_config_valid(self) -> bool:
        """Checks if the twitch values are valid"""
        return all(
            getattr(self.get_twitch_data(), value.name) is not None
            for value in fields(self.get_twitch_data())
        )

    def is_mega_config_valid(self) -> bool:
        """Checks if the mega values are valid"""
        return all(
            getattr(self.get_mega_data(), value.name) is not None
            for value in fields(self.get_mega_data())
        )
