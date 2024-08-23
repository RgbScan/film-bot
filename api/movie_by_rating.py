import requests
from api.kinopoisk import base_url, headers
from pprint import pprint


def sort_rating(num_sort: str):
    num_sort = num_sort.split(",")

    for i, v in enumerate(num_sort):
        num_sort[i] = float(v)

    search_name_url = "/v1.4/movie"
    search_params = {
        "page": 1,
        "limit": 5,
        "selectFields": [
            "name",
            "shortDescription",
            "rating",
            "year",
            "genres",
            "ageRating",
            "poster"
        ],
        "rating.kp": num_sort,
        "sortField": [
            "rating.kp"
        ],
        "sortType": "1"
    }

    response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
    res = response.json()['docs']
    print_res = []
    if len(res) == 0:
        return 0
    else:
        for i in res:
            print_res.append(
                f"Название: {i['name']}\n"
                f"Описание: {i['shortDescription']}\n"
                f"Рейтинг кинопоиска: {i['rating']['kp']}\n"
                f"Год производства: {i['year']}\n"
                f"Жанр: {i['genres']}\n"
                f"Возрастной рейтинг: {i['ageRating']}+\n"
                f"Постер: {i['poster']}"
            )
    return print_res
