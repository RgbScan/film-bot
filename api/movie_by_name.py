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
            f"Название: {res['name']}\n"
            f"Описание: {res['shortDescription']}\n"
            f"Рейтинг кинопоиска: {res['rating']['kp']}\n"
            f"Год производства: {res['year']}\n"
            f"Жанр: {genres}\n"
            f"Возрастной рейтинг: {res['ageRating']}+\n"
            f"Постер: {res['poster']}"
        )
