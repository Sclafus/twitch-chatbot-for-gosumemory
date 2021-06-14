import requests
from time import sleep

url = "http://127.0.0.1:24050/json"
while True:

    try:
        result = requests.get(url).json()
        beatmap_id = result['menu']['bm']['id']
        beatmap_url = f"https://osu.ppy.sh/b/{beatmap_id}"
        beatmap_title = result['menu']['bm']['metadata']['title']
        print(f"{beatmap_title} --- {beatmap_url}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to gosumemory socket!")
        break

    sleep(1)