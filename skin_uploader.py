import os
import json

from mega import Mega
from zipfile import ZipFile
from utils import mega_env, colors, get_data


def get_skin_url() -> str:
    '''
        Returns the current skin url from mega
        If skin isn't uploaded into the mega folder, 
        it is zipped and then uploaded to the mega folder specified in the .env
    '''
    # checking env
    if [True for match in mega_env.values() if match in ['', None]]:
        print(f"{colors.RED}Your .env is not valid or missing.")
        exit()

    # getting skin name and skin path from gosumemory
    api_data = get_data()
    if api_data:
        skin_name = api_data['settings']['folders']['skin']
        osu_path = api_data['settings']['folders']['game']
        skin_folder_path = os.path.join(osu_path, os.path.join('Skins', skin_name))

    # check if the json file exists 
    skins_dict = {}
    if os.path.exists(os.path.join(os.path.abspath(os.getcwd()), 'skins.json')): 
        with open("skins.json", "r") as jsonFile:
            skins_dict = json.load(jsonFile)
            skin_url = skins_dict.get(skin_name)
            if skin_url:
                return skin_url
    else:
        with open("skins.json","w") as jsonFile: jsonFile.write("{}")
    
    # logging into mega account
    mega = Mega()
    mega_email = mega_env['MEGA_EMAIL']
    mega_password = mega_env['MEGA_PASSWORD']
    m = mega.login(mega_email, mega_password)

    mega_file = m.find(f"{skin_name}.osk")
    mega_folder = mega_env['MEGA_OSUSKIN_FOLDER']

    if not mega_file:
        # zipping the skin folder as skin_name.osk
        with ZipFile(f"{skin_name}.osk", 'w') as zf:
            for root, dirs, files in os.walk(f"{skin_folder_path}"):
                for file in files:
                    zf.write(os.path.join(root, file))

        # uploading skin_name.osk to mega
        mega_skin = m.upload(f"{skin_name}.osk", mega_folder[0])
        skin_url = m.get_upload_link(mega_skin)
        
        skins_dict[skin_name] = skin_url
        with open("skins.json", "w") as jsonFile:
            json.dump(skins_dict, jsonFile)

        # removing the local zip file
        os.remove(f"{skin_name}.osk")

        return skin_url

    print(f"{colors.YELLOW}The skin is already on mega!")
    skin_url = m.get_link(mega_file)
    skins_dict[skin_name] = skin_url
    with open("skins.json", "w") as jsonFile:
        json.dump(skins_dict, jsonFile)
    return skin_url