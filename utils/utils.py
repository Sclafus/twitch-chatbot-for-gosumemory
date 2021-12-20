"""
Init module for colors and config handler
"""

import os
import json
from zipfile import ZipFile
from json import load, dump

from requests import get
from bs4 import BeautifulSoup


def tinyurl_shortener(full_url: str) -> str:
    """Returns a shortened url for the provided url."""

    api = "https://tinyurl.com/api-create.php"
    params = {"url": full_url}
    return get(api, params).text


def zip_skin(skin_name: str, skin_folder_path: str) -> dict:
    """Zips the specified skin in a .osk file from the folder defined."""

    with ZipFile(f"{skin_name}.osk", "w") as zip_file:
        for root, _, files in os.walk(skin_folder_path):
            for file in files:
                zip_file.write(
                    os.path.join(root, file),
                    arcname=os.path.relpath(os.path.join(root, file), skin_folder_path),
                )


def get_map_infos(url: str):
    """Gets the map info using web scraping."""

    # scraping
    webpage = get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    tag = soup.find(id="json-beatmapset")

    if not tag:
        return None

    # loading data as json
    json_data = json.loads(tag.contents[0])
    # diffs_data = json_data['beatmaps']

    # getting top diff when a set is passed
    # diffs = []
    # for diff_data in diffs_data:
    #     diffs.append({
    #         'name': diff_data['version'],
    #         'stars': diff_data['difficulty_rating'],
    #         'id': diff_data['id'],
    #         'bpm': diff_data['bpm'],
    #         'ar': diff_data['ar'],
    #         'cs': diff_data['cs']
    #     })
    # diffs = [{'name': diff_data['version'],
    #           'stars': diff_data['difficulty_rating'],
    #           'id': diff_data['id'],
    #           'bpm': diff_data['bpm'],
    #           'ar': diff_data['ar'],
    #           'cs': diff_data['cs']
    #     } for diff_data in json_data['beatmaps']]

    # finding top diff
    diff = max(
        [
            {
                "name": diff_data["version"],
                "stars": diff_data["difficulty_rating"],
                "id": diff_data["id"],
                "bpm": diff_data["bpm"],
                "ar": diff_data["ar"],
                "cs": diff_data["cs"],
            }
            for diff_data in json_data["beatmaps"]
        ],
        key=lambda x: x["stars"],
    )

    return {"artist": json_data["artist"], "title": json_data["title"], "diff": diff}


def add_element_to_json_file(filename: str, key: str, value, encoding: str = "utf-8"):
    """add specified key value pair to json file"""
    if not os.path.exists(os.path.join(os.path.abspath(os.getcwd()), filename)):
        return

    _dict = {}
    with open(filename, "r", encoding=encoding) as json_file:
        _dict = load(json_file)

    _dict[key] = value
    with open(filename, "w", encoding=encoding) as json_file:
        dump(_dict, json_file, indent=4)
