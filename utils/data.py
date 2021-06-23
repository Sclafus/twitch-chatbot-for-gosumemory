'''
Helper module to get data from gosumemory, mega and from the .env file
'''

import requests

from dotenv import load_dotenv
from os.path import join, dirname, realpath
from os import pardir, environ
from utils import colors


class Data:
    '''
        Data handler using the .env file
        and gosumemory json to return data for
        the main program.
    '''

    def __init__(self):
        ''' Class constructor, loads the .env file. '''

        load_dotenv(join(join(dirname(realpath(__file__)), pardir), '.env'))

        self._twitch_env = {
            "TMI_TOKEN": environ.get('TMI_TOKEN'),
            "CLIENT_ID": environ.get('CLIENT_ID'),
            "BOT_NICK": environ.get('BOT_NICK'),
            "BOT_PREFIX": environ.get('BOT_PREFIX'),
            "CHANNEL": environ.get('CHANNEL'),
            "GOSUMEMORY_JSON": environ.get('GOSUMEMORY_JSON_URL')
        }

        self._mega_env = {
            "MEGA_EMAIL": environ.get('MEGA_EMAIL'),
            "MEGA_PASSWORD": environ.get('MEGA_PASSWORD'),
            "MEGA_FOLDER": environ.get('MEGA_FOLDER')
        }

    def get_mega_data(self) -> dict:
        ''' Returns mega .env data. '''

        return self._mega_env

    def get_twitch_data(self) -> dict:
        ''' Returns twitch .env data. '''

        return self._twitch_env

    def get_gosumemory_data(self) -> dict:
        ''' 
            Gets data from gosumemory, returns a dictionary
            with every information contained in the gosumemory json.
        '''

        try:
            # get data from gosumemory
            api_data = requests.get(self.get_twitch_data()[
                                    'GOSUMEMORY_JSON']).json()
            return api_data if 'error' not in api_data else None

        except requests.exceptions.ConnectionError as err:
            # error handling, can't connect to gosumemory
            print(f"{colors.RED}Could not connect to gosumemory socket!")
            return None

    def get_skin(self) -> dict:
        ''' Gets data from gosumemory, returns skin informations. '''

        from skin_uploader import get_skin_url

        api_data = self.get_gosumemory_data()
        if api_data:

            skin_name = api_data['settings']['folders']['skin']
            skin_url = get_skin_url()

            return {
                "skin": skin_name,
                "url": skin_url
            }
        return None

    def get_map(self) -> dict:
        ''' Gets data from gosumemory, returns current beatmap informations. '''

        api_data = self.get_gosumemory_data()
        if api_data:
            # creating download link
            beatmap_id = api_data['menu']['bm']['id']
            beatmap_url = f"https://osu.ppy.sh/b/{beatmap_id}"

            beatmap_metadata = api_data['menu']['bm']['metadata']
            return {
                "url": beatmap_url,
                "title": beatmap_metadata['title'],
                "artist": beatmap_metadata['artist'],
                "diff": beatmap_metadata['difficulty'],
                "mapper": beatmap_metadata['mapper']
            }
        return None
