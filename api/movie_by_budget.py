import requests
from kinopoisk import base_url, headers
from pprint import pprint

search_name_url = "/v1.4/movie"
search_params = {
    "page": 1,
    "limit": 5,
    "selectFields": [
        "name",
        "rating",
        "year",
        "genres",
        "ageRating",
        "poster",
        "budget"
    ],
    "sortField": [
        "budget.value"
    ],
    'sortType': ""
}


def sort_type(type_sort):
    if type_sort == "1":
        search_params["sortType"] = "1"
    elif type_sort == "-1":
        search_params["sortType"] = "-1"


# По возрастанию (фильмы с низким бюджетом)
sort_type("1")


# По убыванию (фильмы с высоким бюджетом)
#sort_type("-1")


response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
res = response.json()
pprint(res)

