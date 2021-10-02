from os import stat
import re

class Osu:

    @staticmethod
    def is_map_request(message: str):
        return True if re.findall(r'https?:\/\/osu.ppy.sh\/(b|beatmaps|beatmapsets)\/[\d]+', message) else False