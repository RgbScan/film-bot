import requests
from api.kinopoisk import base_url, headers


def sort_rating(num_sort: list):
    search_name_url = "/v1.4/movie"
    search_params = {
        "page": 1,
        "limit": 12,
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
    res = response.json()['docs'][0]
    if len(res) == 0:
        return "К сожалению не удалось выполнить сортировку"
    else:
        genres = []
        for x in res['genres']:
            genres.append(x['name'])
        return (
            f"Название: {res['name']}\n"
            f"Описание: {res['shortDescription']}\n"
            f"Рейтинг кинопоиска: {res['rating']['kp']}\n"
            f"Год производства: {res['year']}\n"
            f"Жанр: {genres}\n"
            f"Возрастной рейтинг: {res['ageRating']}+\n"
            f"Постер: {res['poster']}"
        )

