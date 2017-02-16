import json

name_f = input("Enter film and I'll give you better one: ")

with open('films.json', encoding='utf-8') as data_file:
    films = json.load(data_file)


def find_info_film_if_in_base(name):
    """
    Находит всю информацию о фильме, если фильм с таким названием есть в базе
    :param name: название фильма
    :return: возвращает словарь фильма с данным названием, если он есть в базе,
             None, если нет
    """
    i = 0
    name = name.lower()
    while i < 1000 and name != films[i]['original_title'].lower():
        i += 1
    if i != 1000:
        return films[i]


def count_of_same_word(text1, text2):
    """
    Подсчитывает количество общих слов в двух переменных типа string
    :return: integer
    """
    count_of_words = 0
    text1 = text1.lower()
    for word in text1.split(' '):
        if len(word) > 2 and word in text2.lower():
            count_of_words += 1
    return count_of_words


def calculate_weight(title, overview, pr_comp, genres, rating):
    """
    Рассчитывает "вес" фильма исходя из его схожести с данным фильмом
    по разным параметрам
    :param title: количество общих слов в названиях двух фильмов
    :param overview: количество общих слов в описаниях двух фильмов
    :param pr_comp: количество общих кинокомпаний двух фильмов
    :param genres: количество общих жанров двух фильмов
    :param adult: совпадение возрастного ограничения (boolean)
    :param rating: рейтинг фильма
    :return: double
    """
    weight = 0
    weight += 2 * title
    weight += 2 * overview
    weight += 4 * pr_comp
    weight += 7 * genres
    weight += rating * 1.2
    return weight


def recommendate_for_film_in_base(film):
    """
    Находит фильмы, схожие с данным, если данный фильм есть в базе
    :param film: словарь фильма из базы
    :return: dictionary, key - tuple of name of film and its id
                         value - weight
    """
    id_f = film['id']
    name = film['original_title']
    overview = film['overview']
    prod_comp = set([i['id'] for i in film['production_companies']])
    genres = set([i['id'] for i in film['genres']])

    weights = {}

    for f in films:
        same_words_in_title = count_of_same_word(name, f['original_title'])
        same_words_in_overview = count_of_same_word(overview, f['overview'])
        same_pr_comp = len(prod_comp & \
                       set([i['id'] for i in f['production_companies']]))
        same_genres = len(genres & \
                      set([i['id'] for i in f['genres']]))

        weight = calculate_weight(same_words_in_title, same_words_in_overview,
                   same_pr_comp, same_genres, f['vote_average'])
        key = (f['original_title'], f['id'])

        if weight > 20 and id_f != f['id']:
            weights[key] = weight

    return weights


def recommendate_by_name(name):
    """
    Если фильма с данным названием нет в базе, то используется эта функция,
    которая выдает фильмы с схожим названием
    :param name:
    :param films:
    """
    name = name.lower()
    films_with_similar_name = {}
    for film in films:
        count = count_of_same_word(name, film["original_title"])
        if count > 1 or count > len(name.split()) - 1:
            if film['original_title'].lower() != name:
                films_with_similar_name[film['original_title']] = count
    for key, val in sorted(films_with_similar_name.items(),
                           key=lambda x: x[1], reverse=True)[0:7]:
        print(key)


film_info = find_info_film_if_in_base(name_f)
if film_info: # Если фильм есть в базе
    films = recommendate_for_film_in_base(film_info)
    for film, weight in sorted(films.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(film[0])
else:
    recommendate_by_name(name_f)

