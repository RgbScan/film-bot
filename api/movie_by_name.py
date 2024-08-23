import requests
from api.kinopoisk import base_url, headers


def search_film(name_movie):
    search_name_url = "/v1.4/movie/search"
    search_params = {
        "page": 1,
        "limit": 12,
        "query": name_movie
    }

    response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
    res = response.json()['docs'][0]
    if len(res) == 0:
        return f"К сожалению фильм {name_movie} не найден"
    else:
        genres = []
        for x in res['genres']:
            genres.append(x['name'])
        return(
            f"Название: {res.get('name') or 'Не указано'}\n"
            f"Описание: {res.get('shortDescription') or 'Не указано'}\n"
            f"Рейтинг imdb: {res['rating'].get('imdb') or 'Не указан'}\n"
            f"Год производства: {res.get('year') or 'Не указан'}\n"
            f"Жанр: {', '.join(genres)}\n"
            f"Возрастной рейтинг: {str(res.get('ageRating')) + '+' if res.get('ageRating') else 'Не указан'}\n"
            f"Постер: {res['poster'].get('url', '')}"
        )
