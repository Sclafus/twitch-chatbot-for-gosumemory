'''
Init module for colors and .env handler
'''

import os
from zipfile import ZipFile

from requests import get

def tinyurl_shortener(full_url: str) -> str:
    ''' Returns a shortened url for the provided url. '''

    api = 'https://tinyurl.com/api-create.php'
    params = {'url': full_url}
    return get(api, params).text


def zip_skin(skin_name: str, skin_folder_path: str):
    ''' Zips the specified skin in a .osk file from the folder defined. '''

    with ZipFile(f'{skin_name}.osk', 'w') as zip_file:
        for root, _, files in os.walk(skin_folder_path):
            for file in files:
                zip_file.write(os.path.join(root, file), arcname=os.path.relpath(
                    os.path.join(root, file), skin_folder_path))
