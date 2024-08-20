import requests
from pprint import pprint

API = "Z4XDYZA-W8R40GQ-J9Z8264-N82CT22"
url = "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10"

headers = {
    "accept": "application/json",
    "X-API-KEY": API}

response = requests.get(url, headers=headers)

pprint(response.text)

