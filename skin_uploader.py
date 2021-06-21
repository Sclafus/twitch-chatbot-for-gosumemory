import os

from mega import Mega
from zipfile import ZipFile
from utils import mega_env, colors, get_data


def get_skin_url() -> str:
    # checking env
    if [True for match in mega_env.values() if match in ['', None]]:
        print(f"{colors.RED}Your .env is not valid or missing.")
        exit()

    # logging into mega account
    mega = Mega()
    mega_email = mega_env['MEGA_EMAIL']
    mega_password = mega_env['MEGA_PASSWORD']
    m = mega.login(mega_email, mega_password)

    # getting skin name and skin path from gosumemory
    api_data = get_data()
    if api_data:
        skin_name = api_data['settings']['folders']['skin']
        osu_path = api_data['settings']['folders']['game']
        skin_folder_path = os.path.join(osu_path, os.path.join('Skins', skin_name))

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
        public_link = m.get_upload_link(mega_skin)

        # removing the local zip file
        os.remove(f"{skin_name}.osk")

        return public_link

    print(f"{colors.YELLOW}The skin is already on mega!")
    public_link = m.get_link(mega_file)
    return public_link