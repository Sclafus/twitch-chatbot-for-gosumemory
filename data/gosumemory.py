"""
Helper module to get data from gosumemory, mega and from the config file
"""

from os.path import join
from os import pardir, remove

import requests
from file_sharing.mega_handler import MegaHandler

from outputs.outputs import Outputs
from utils.utils import zip_skin, tinyurl_shortener, add_element_to_json_file, create_empty_json_file, search_json_file
from .config import Config


class Gosumemory:
    """Gosumemory class, used to get data from the gosumemory api"""

    def __init__(self):
        """Class constructor, loads the config file."""
        self._config = Config()
        self.gosumemory_url = self._config.get_gosumemory_url()

    def get_gosumemory_data(self) -> dict:
        """
        Gets data from gosumemory, returns a dictionary
        with every information contained in the gosumemory json.
        """

        try:
            # get data from gosumemory
            api_data = requests.get(self.gosumemory_url).json()
            return api_data if "error" not in api_data else None

        except requests.exceptions.ConnectionError:
            # error handling, can't connect to gosumemory
            return None

    def get_skin_url(self, skin_name: str, auto_upload: bool = False) -> str:
        """
        Returns the current skin url from mega.
        If skin isn't uploaded into the mega folder,
        it is zipped and then uploaded to the mega
        folder specified in the config file.
        """

        # getting skin name and skin path from gosumemory
        api_data = self.get_gosumemory_data()

        # can't fetch api data, exit
        if not api_data:
            return None

        skin_folder_path = join(
            join(api_data["settings"]["folders"]["songs"], pardir),
            join("Skins", skin_name),
        )

        # creating empty json for skins only if necessary
        create_empty_json_file("skins.json")

        # if the url is already present in skins.json, return it
        if skin_url := search_json_file("skins.json", key=skin_name):
            return skin_url

        # url not in json, auto upload disabled, return
        if not auto_upload:
            return None

        mega_credentials = self._config.get_mega_data()

        # logging into mega account
        mega = MegaHandler(
            mega_credentials["MEGA_EMAIL"], mega_credentials["MEGA_PASSWORD"]
        )
        skin_file_mega = mega.find(f"{skin_name}.osk")

        skin_mega_folder = mega.find(f"{mega_credentials['MEGA_FOLDER']}/Skins")

        # can't find the specified mega folder, creating it
        if not skin_mega_folder:
            mega.create_folder(f'{mega_credentials["MEGA_FOLDER"]}/Skins')

        # skin is already on mega
        if skin_file_mega:
            Outputs.print_info("The skin is already on mega!")
            skin_url_short = tinyurl_shortener(mega.get_link(skin_file_mega))
            add_element_to_json_file("skins.json", skin_name, skin_url_short)
            return skin_url_short

        # the skin is not on mega

        # zipping the skin folder as skin_name.osk
        Outputs.print_info("Zipping your current skin")
        zip_skin(skin_name, skin_folder_path)

        # uploading skin_name.osk to mega
        Outputs.print_info("Uploading your current skin")
        skin_url = mega.upload_file(
            f"{skin_name}.osk", f"{mega_credentials['MEGA_FOLDER']}/Skins"
        )
        Outputs.print_info("Your current skin has been uploaded to mega")

        # removing the local zip file
        remove(f"{skin_name}.osk")

        # shortening
        skin_url_short = tinyurl_shortener(skin_url)
        add_element_to_json_file("skins.json", skin_name, skin_url_short)

        # dumping the url to the json file
        return skin_url_short

    def get_skin(self, url_support: bool = True) -> dict:
        """Gets data from gosumemory, returns skin informations."""

        api_data = self.get_gosumemory_data()
        if not api_data:
            return None

        skin_name = api_data["settings"]["folders"]["skin"]
        skin_url = (
            self.get_skin_url(skin_name, self._config.is_mega_config_valid())
            if url_support
            else "private"
        )

        return {"skin": skin_name, "url": skin_url}

    def get_map(self) -> dict:
        """Gets data from gosumemory, returns current beatmap informations."""

        api_data = self.get_gosumemory_data()
        if not api_data:
            return None

        # creating download link

        beatmap_metadata = api_data["menu"]["bm"]["metadata"]
        return {
            "url": f"https://osu.ppy.sh/b/{api_data['menu']['bm']['id']}",
            "title": beatmap_metadata["title"],
            "artist": beatmap_metadata["artist"],
            "diff": beatmap_metadata["difficulty"],
            "mapper": beatmap_metadata["mapper"],
        }


gosumemory = Gosumemory()
