''' Colors package'''

import colorama

colorama.init(autoreset=True)


class Colors:
    ''' Color handler '''
    # pylint: disable=too-few-public-methods

    # colors
    NOCOLOR = "\033[0m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    LIGHT_PURPLE = "\033[95m"


colors = Colors()
