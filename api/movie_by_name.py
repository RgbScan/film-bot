import requests
from kinopoisk import base_url, headers

search_name_url = "/v1.4/movie/search"
search_params = {
    "page": 1,
    "limit": 12,
    "query": "пятый элемент"
}

response = requests.get(base_url + search_name_url, headers=headers, params=search_params)
res = response.json()['docs'][0]
genres = []
for x in res['genres']:
    genres.append(x['name'])

print(
    f"Название: {res['name']}\n"
    f"Описание: {res['shortDescription']}\n"
    f"Рейтинг кинопоиска: {res['rating']['kp']}\n"
    f"Год производства: {res['year']}\n"
    f"Наверно жанр: {genres}\n"
    f"Возрастной рейтинг: {res['ageRating']}+\n"
    f"Постер: {res['poster']}"
)