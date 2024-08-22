import os
import requests
from dotenv import load_dotenv

load_dotenv()


base_url = "https://api.kinopoisk.dev/"
headers = {
    "X-API-KEY": os.getenv("API_TOKEN"),
    "accept": "application/json"
}


