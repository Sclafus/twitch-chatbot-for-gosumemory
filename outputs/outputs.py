'''Output handler module'''
from outputs.colors import Color


class Outputs():
    '''output class, used to display some text in the terminal'''

    @staticmethod
    def print_message(author: str, message: str) -> None:
        '''prints a chat message to the terminal with colors'''
        print(
            f"{Color.LIGHT_PURPLE.value}{author}: {Color.NOCOLOR.value}{message}")

    @staticmethod
    def print_info(to_be_printed: str) -> None:
        '''prints a info message to the terminal with colors'''
        print(f"{Color.CYAN.value}{to_be_printed}{Color.NOCOLOR.value}")

    @staticmethod
    def print_error(error: str) -> None:
        '''prints an error message to the terminal with colors'''
        print(f"{Color.RED.value}{error}{Color.NOCOLOR.value}")

    @staticmethod
    def print_warning(warning: str) -> None:
        '''prints an error message to the terminal with colors'''
        print(f"{Color.YELLOW.value}{warning}{Color.NOCOLOR.value}")

    @staticmethod
    def print_map_request(author: str, message: str) -> None:
        '''prints an osu map request to the terminal with colors'''
        # TODO
        return

    @staticmethod
    def string_map(metadata: dict) -> str:
        '''returns a formatted string for osu maps'''
        # FIXME should not be here
        return (f"/me {metadata['artist']} - {metadata['title']} "
                f"[{metadata['diff']}] by {metadata['mapper']} | "
                f"Link: {metadata['url']}")
