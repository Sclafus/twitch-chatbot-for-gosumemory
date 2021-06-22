import os
import json

from mega import Mega
from utils import data, colors
from requests import get
from zipfile import ZipFile


def tinyurl_shortener(full_url: str) -> str:
    '''Returns a shortened url for the provided url'''
    api = 'https://tinyurl.com/api-create.php'
    params = {'url': full_url}
    return get(api, params).text


def zip_skin(skin_name: str, skin_folder_path: str):
    with ZipFile(f'{skin_name}.osk', 'w') as zf:
        for root, _, files in os.walk(f'{skin_folder_path}'):
            for file in files:
                zf.write(os.path.join(root, file))


def get_skin_url() -> str:
    '''
        Returns the current skin url from mega
        If skin isn't uploaded into the mega folder,
        it is zipped and then uploaded to the mega folder specified in the .env
    '''

    # getting skin name and skin path from gosumemory
    api_data = data.get_gosumemory_data()

    # can't fetch api data, exit
    if not api_data:
        return

    skin_name = api_data['settings']['folders']['skin']
    osu_path = os.path.join(
        api_data['settings']['folders']['songs'], os.pardir)
    skin_folder_path = os.path.join(
        osu_path, os.path.join('Skins', skin_name))

    # check if the json file exists
    if not os.path.exists(os.path.join(os.path.abspath(os.getcwd()), 'skins.json')):
        with open('skins.json', 'w') as jsonFile:
            jsonFile.write("{}")

    skins_dict = {}
    with open('skins.json', 'r') as jsonFile:
        skins_dict = json.load(jsonFile)
        skin_url = skins_dict.get(skin_name)
        if skin_url:
            return skin_url

    # checking env
    mega_credentials = data.get_mega_data()
    if [True for match in mega_credentials.values() if match in ['', None]]:
        print(f'''{colors.YELLOW}Your .env is missing Mega values.
            It will not be able to upload the skin automatically.''')
        return

    # logging into mega account
    mega = Mega()
    mega_email = mega_credentials['MEGA_EMAIL']
    mega_password = mega_credentials['MEGA_PASSWORD']
    m = mega.login(mega_email, mega_password)

    mega_file = m.find(f'{skin_name}.osk', exclude_deleted=True)
    mega_folder = m.find(mega_credentials['MEGA_FOLDER'])

    # can't find the specified mega folder, creating it
    if not mega_folder:
        print(
            f"{colors.YELLOW}Can't find the specified folder on mega, creating a new one")
        mega_folder = m.create_folder(mega_credentials['MEGA_FOLDER'])
        return "please run the command again to get the URL!"

    # the skin is not on mega
    if not mega_file:

        # zipping the skin folder as skin_name.osk
        print(f"{colors.CYAN}Zipping your current skin")
        zip_skin(skin_name, skin_folder_path)

        # uploading skin_name.osk to mega
        print(f"{colors.CYAN}Uploading your current skin")
        mega_skin = m.upload(f"{skin_name}.osk", mega_folder[0])
        skin_url = m.get_upload_link(mega_skin)
        print(f"{colors.CYAN}Your current skin has been uploaded to mega")

        # removing the local zip file
        os.remove(f'{skin_name}.osk')

        # shortening
        skin_url_short = tinyurl_shortener(skin_url)

        # dumping the url to the json file
        skins_dict[skin_name] = skin_url_short
        with open('skins.json', 'w') as json_file:
            json.dump(skins_dict, json_file, indent=4)

        return skin_url_short

    # the skin is on mega
    print(f"{colors.YELLOW}The skin is already on mega!")
    skin_url = m.get_link(mega_file)

    # shortening
    skin_url_short = tinyurl_shortener(skin_url)
    skins_dict[skin_name] = skin_url_short

    # dumping the url to the json file
    with open('skins.json', 'w') as json_file:
        json.dump(skins_dict, json_file, indent=4)

    return skin_url_short
