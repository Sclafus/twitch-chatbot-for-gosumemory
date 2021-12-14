from .colors import colors

class Outputs():
    '''output class, used to display some text in the terminal'''

    @staticmethod
    def print_message(author: str, message: str) -> None:
        '''prints a chat message to the terminal with colors'''
        print(f"{colors['LIGHT_PURPLE']}{author}: {colors['NOCOLOR']}{message}")

    @staticmethod
    def print_info(to_be_printed: str) -> None:
        '''prints a info message to the terminal with colors'''
        print(f"{colors['CYAN']}{to_be_printed}{colors['NOCOLOR']}")

    @staticmethod
    def print_error(error: str) -> None:
        '''prints an error message to the terminal with colors'''
        print(f"{colors['RED']}{error}{colors['NOCOLOR']}")

    @staticmethod
    def print_map_request(author: str, message: str) -> None:
        '''prints an osu map request to the terminal with colors'''
        # TODO

    @staticmethod
    def string_map(metadata: dict) -> str:
        '''returns a formatted string for osu maps'''
        # FIXME should not be here
        return (f"/me {metadata['artist']} - {metadata['title']} "
                f"[{metadata['diff']}] by {metadata['mapper']} | "
                f"Link: {metadata['url']}")
