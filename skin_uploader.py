import os

from mega import Mega
from zipfile import ZipFile
from utils import mega_env, colors, get_data

# checking env
if [True for match in mega_env.values() if match in ['', None]]:
    print(f"{colors.RED}Your .env is not valid or missing.")
    exit()

# logging into mega account
mega = Mega()
email = mega_env['MEGA_EMAIL']
password = mega_env['MEGA_PASSWORD']
m = mega.login(email, password)

# getting skin name from gosumemory
api_data = get_data()
if api_data:
   skin_name = api_data['settings']['folders']['skin']
   osu_path = api_data['settings']['folders']['game']
   skin_folder_path = os.path.join(osu_path, os.path.join('Skins', skin_name))

mega_file = m.find(f"{skin_name}.osk")
mega_folder = m.find('Osu! Skins')

if mega_file:
    print(f"{colors.YELLOW}The skin is already on mega!")
else: 
    # zipping the skin folder as skin_name.osk
    zip_skin = ZipFile(f"{skin_name}.osk", 'w')
    for root, dirs, files in os.walk(f"{skin_folder_path}"):
        for file in files:
            zip_skin.write(os.path.join(root, file))
    zip_skin.close()

    # uploading to mega
    mega_skin = m.upload(f"{skin_name}.osk", mega_folder[0])
    public_link = m.get_upload_link(f"{skin_name}.osk")

    os.remove(f"{skin_name}.osk")