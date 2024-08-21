import requests
from kinopoisk import base_url, headers
from pprint import pprint

search_name_url = "/v1.4/movie"
search_params = {
    "page": 1,
    "limit": 12,
    "selectFields": [
        "name",
        "rating",
        "year",
        "genres",
        "ageRating",
        "poster"
    ],
    "rating.kp": [
        7,
        8,
    ]
}

response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
res = response.json()
pprint(res)

