import requests
import os
import colorama
from dotenv import load_dotenv

# colors
colorama.init(autoreset=True)
class Colors:
    NOCOLOR = "\033[0m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    LIGHT_PURPLE = "\033[95m"

colors = Colors()

# loading env
load_dotenv(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), '.env'))
twitch_chatbot_env = {
    "TMI_TOKEN": os.environ.get('TMI_TOKEN'),
    "CLIENT_ID": os.environ.get('CLIENT_ID'),
    "BOT_NICK": os.environ.get('BOT_NICK'),
    "BOT_PREFIX": os.environ.get('BOT_PREFIX'),
    "CHANNEL": os.environ.get('CHANNEL'),
    "GOSUMEMORY_JSON": os.environ.get('GOSUMEMORY_JSON_URL')
}
mega_env = {
    "MEGA_EMAIL": os.environ.get('MEGA_EMAIL'),
    "MEGA_PASSWORD": os.environ.get('MEGA_PASSWORD')
}

def get_data() -> dict:
    try:
        # get data from gosumemory
        api_data = requests.get(twitch_chatbot_env['GOSUMEMORY_JSON']).json()
        return api_data if 'error' not in api_data else None

    except requests.exceptions.ConnectionError:
        # error handling, can't connect to gosumemory
        print(f"{colors.RED}Could not connect to gosumemory socket!")
        return None
