'''
Helper module to get data from gosumemory, mega and from the config file
'''

from os.path import join, abspath, exists
from os import pardir, getcwd, remove
from json import load, dump

import requests
from mega import Mega

from outputs.outputs import Outputs
from utils.utils import zip_skin, tinyurl_shortener
from .config import Config


class Gosumemory:
    '''Gosumemory class, used to get data from the gosumemory api'''

    def __init__(self):
        ''' Class constructor, loads the config file. '''
        self._config = Config()
        self.gosumemory_url = self._config.GOSUMEMORY_JSON

    def get_gosumemory_data(self) -> dict:
        '''
            Gets data from gosumemory, returns a dictionary
            with every information contained in the gosumemory json.
        '''

        try:
            # get data from gosumemory
            api_data = requests.get(self.gosumemory_url).json()
            return api_data if 'error' not in api_data else None

        except requests.exceptions.ConnectionError:
            # error handling, can't connect to gosumemory
            Outputs.print_error("Could not connect to gosumemory socket!")
            return None

    # TODO refactor and move mega stuff to a method
    def get_skin_url(self) -> str:
        '''
            Returns the current skin url from mega.
            If skin isn't uploaded into the mega folder,
            it is zipped and then uploaded to the mega
            folder specified in the config file.
        '''

        # getting skin name and skin path from gosumemory
        api_data = self.get_gosumemory_data()

        # can't fetch api data, exit
        if not api_data:
            return None

        skin_name = api_data['settings']['folders']['skin']
        skin_folder_path = join(join(
            api_data['settings']['folders']['songs'], pardir), join('Skins', skin_name))

        # check if the json file exists
        if not exists(join(abspath(getcwd()), 'skins.json')):
            with open('skins.json', 'w', encoding='utf-8') as json_file:
                json_file.write("{}")

        skins_dict = {}
        with open('skins.json', 'r', encoding='utf-8') as json_file:
            skins_dict = load(json_file)
            skin_url = skins_dict.get(skin_name)
            if skin_url:
                return skin_url

        # checking env
        mega_credentials = self._config.get_mega_data()
        if [True for match in mega_credentials.values() if match in ['', None]]:
            Outputs.print_warning("Your config is missing Mega values."
                                  "It will not be able to upload the skin automatically.")
            return None

        # logging into mega account
        mega_connection = Mega().login(mega_credentials['MEGA_EMAIL'],
                                       mega_credentials['MEGA_PASSWORD'])

        mega_file = mega_connection.find(
            f'{skin_name}.osk', exclude_deleted=True)
        mega_folder = mega_connection.find(mega_credentials['MEGA_FOLDER'])

        # can't find the specified mega folder, creating it
        if not mega_folder:
            Outputs.print_warning(
                "Can't find the specified folder on mega, creating a new one")
            mega_folder = mega_connection.create_folder(
                mega_credentials['MEGA_FOLDER'])
            return "Please run the command again to get the URL!"

        # the skin is not on mega
        if not mega_file:

            # zipping the skin folder as skin_name.osk
            Outputs.print_info("Zipping your current skin")
            zip_skin(skin_name, skin_folder_path)

            # uploading skin_name.osk to mega
            Outputs.print_info("Uploading your current skin")
            mega_skin = mega_connection.upload(
                f"{skin_name}.osk", mega_folder[0])
            skin_url = mega_connection.get_upload_link(mega_skin)
            Outputs.print_info("Your current skin has been uploaded to mega")

            # removing the local zip file
            remove(f'{skin_name}.osk')

            # shortening
            skin_url_short = tinyurl_shortener(skin_url)

            # dumping the url to the json file
            skins_dict[skin_name] = skin_url_short
            with open('skins.json', 'w', encoding='utf-8') as json_file:
                dump(skins_dict, json_file, indent=4)

            return skin_url_short

        # the skin is on mega
        Outputs.print_info("The skin is already on mega!")
        skin_url = mega_connection.get_link(mega_file)

        # shortening
        skin_url_short = tinyurl_shortener(skin_url)
        skins_dict[skin_name] = skin_url_short

        # dumping the url to the json file
        with open('skins.json', 'w', encoding='utf-8') as json_file:
            dump(skins_dict, json_file, indent=4)

        return skin_url_short

    def get_skin(self) -> dict:
        ''' Gets data from gosumemory, returns skin informations. '''

        api_data = self.get_gosumemory_data()
        if api_data:

            skin_name = api_data['settings']['folders']['skin']
            skin_url = self.get_skin_url()

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


gosumemory = Gosumemory()
