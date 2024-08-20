import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


base_url = "https://api.kinopoisk.dev/"
headers = {
    "X-API-KEY": os.getenv("API_TOKEN"),
    "accept": "application/json"
}


