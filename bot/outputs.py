from colors import colors


class Outputs():

    @staticmethod
    def print_message(author: str, message: str) -> None:
        print(f"{colors.LIGHT_PURPLE}{author}: {colors.NOCOLOR}{message}")

    @staticmethod
    def print_warning(to_be_printed: str) -> None:
        print(f"{colors.CYAN}{to_be_printed}")

    @staticmethod
    def print_error(error: str) -> None:
        print(f"{colors.RED}{error}")

    @staticmethod
    def print_map_request(author: str, message: str) -> None:
        # TODO
        pass

    @staticmethod
    def string_map(metadata: dict) -> str:
        return (f"/me {metadata['artist']} - {metadata['title']} "
                f"[{metadata['diff']}] by {metadata['mapper']} | "
                f"Link: {metadata['url']}")
