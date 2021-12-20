"""Abstraction module to use Mega in a cleaner way"""
from mega import Mega


class MegaHandler:
    """Abstraction layer for Mega"""

    def __init__(self, email: str, passwd: str) -> None:
        self._mega_connection = Mega().login(email, passwd)

    def upload_file(self, filename: str, folder: str):
        """Uploads the specified file, returns the url"""
        _folder = self._mega_connection.find(folder)
        return self._mega_connection.get_upload_link(
            self._mega_connection.upload(filename, _folder[0])
        )

    def find(self, filename: str) -> str:
        """Searches the specified filename on mega"""
        return self._mega_connection.find(filename, exclude_deleted=True)

    def create_folder(self, folder_structure: str) -> None:
        """Creates a folder structure on mega from a string"""
        self._mega_connection.create_folder(folder_structure)

    def get_link(self, filename: str) -> str:
        """Gets the url for the specified file"""
        return self._mega_connection.get_link(filename)
