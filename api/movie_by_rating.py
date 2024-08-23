import requests
from api.kinopoisk import base_url, headers


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
            genres = []
            if i.get('genres', '') != '':
                for gen in i.get('genres', ''):
                    genres.append(gen['name'])
            else:
                'Не указан'
            print_res.append(
                f"Название: {i.get('name') or 'Не указано'}\n"
                f"Описание: {i.get('shortDescription') or 'Не указано'}\n"
                f"Рейтинг imdb: {i['rating'].get('imdb') or 'Не указан'}\n"
                f"Год производства: {i.get('year') or 'Не указан'}\n"
                f"Жанр: {', '.join(genres)}\n"
                
                f"Возрастной рейтинг: {str(i.get('ageRating')) + '+' if i.get('ageRating') else 'Не указан'}\n"
                f"Постер: {i['poster'].get('url') or 'Не указано'}"
            )
    return print_res
