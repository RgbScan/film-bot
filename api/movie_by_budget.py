import requests
from api.kinopoisk import base_url, headers


def movie_budget(sort_num):
    if sort_num == "high_budget_sort":
        sort_num = -1
    else:
        sort_num = 1
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
            "poster",
            "budget"
        ],
        "sortField": [
            "budget.value"
        ],
        'sortType': sort_num
    }

    response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
    res = response.json()['docs']
    print_res = []
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
            f"Рейтинг imdb: {i.get('rating', {}).get('imdb', 'Не указан')}\n"
            f"Год производства: {i.get('year') or 'Не указано'}\n"
            f"Жанр: {', '.join(genres)}\n"
            f"Возрастной рейтинг:"
            f"Возрастной рейтинг: {str(i.get('ageRating')) + '+' if i.get('ageRating') else 'Не указан'}\n"
            f"Постер: {i.get('poster', {}).get('url', 'Нет постера')}\n"
            f"Бюджет:"
            f" {i.get('budget', {}).get('value', 'Не указан')}, Валюта:{i.get('budget', {}).get('currency', '')}"
        )


    return print_res

