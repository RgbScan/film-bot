import time
from datetime import datetime
from telegram_bot_pagination import InlineKeyboardPaginator

from peewee import IntegrityError
from telebot.custom_filters import StateFilter
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardRemove

from keyboards.key import gen_budget, gen_start
from config import bot, command_dict
from database.models import RequestStorage, Users
from states.mainState import MyState
from api import movie_by_name, movie_by_rating, movie_by_budget

bot.add_custom_filter(StateFilter(bot))


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        Users.get(Users.user_id == user_id)
        bot.send_message(
            user_id,
            f"Рад вас снова видеть, {first_name}, что будем искать?",
            reply_markup=gen_start(),
        )
    except Users.DoesNotExist:
        Users.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        bot.send_message(
            user_id,
            f"Приветствую {username}, я помогу тебе найти нужный фильм!",
            reply_markup=gen_start(),
        )


def initiate_name_search(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Введите название фильма",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.set_state(message.from_user.id, MyState.state_name, message.chat.id)


# Команда для поиска фильма по названию
@bot.message_handler(commands=["name"])
def handle_name_command(message):
    initiate_name_search(message)


@bot.message_handler(func=lambda message: message.text == "Найти фильм по названию")
def handle_name_text(message):
    initiate_name_search(message)


@bot.message_handler(state=MyState.state_name)
def push_res(message):
    RequestStorage.create(
        user_id=message.from_user.id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=f"Поиск фильма по названию: {message.text}"
    )

    bot.send_message(
        message.from_user.id,
        movie_by_name.search_film(message.text)
    )
    bot.delete_state(message.from_user.id, message.chat.id)


def initiate_rating_search(message):
    bot.send_message(
        message.from_user.id,
        "Введите значение для поиска."
        "\nВы можете ввести одно значение, например: 5.5 или 8."
        "\nИли можете ввести сразу несколько значений через запятую, например: 5, 6.5, 8, 7",
    )
    bot.set_state(message.from_user.id, MyState.state_rating, message.chat.id)


@bot.message_handler(commands=["rating"])
def handle_rating_command(message):
    initiate_rating_search(message)


@bot.message_handler(func=lambda message: message.text == "Найти фильм по рейтингу")
def handle_rating_text(message):
    initiate_rating_search(message)


# Глобальный словарь для хранения отсортированных фильмов по user_id
user_movies = {}


@bot.message_handler(state=MyState.state_rating)
def sort_max_to_min(message):
    user_id = message.from_user.id

    # Сортируем фильмы по рейтингу и сохраняем результат в словаре
    sorted_movies = movie_by_rating.sort_rating(message.text)
    user_movies[user_id] = sorted_movies

    if not sorted_movies:
        bot.send_message(
            message.from_user.id,
            "К сожалению не удалось найти фильмы с таким рейтингом"
        )
    else:
        # Отправляем первую страницу с результатами
        send_paginated_message(message.chat.id, sorted_movies, 1)

    bot.delete_state(message.from_user.id, message.chat.id)


def send_paginated_message(chat_id, movie_list, page, message_id=None):
    items = len(movie_list)
    items_per_page = 1
    total_pages = (items // items_per_page) + (1 if items % items_per_page > 0 else 0)

    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=page,
        data_pattern='page#{page}'
    )

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_items = movie_list[start:end]

    text = "\n".join(map(str, page_items))

    if message_id:
        # Обновляем текст и клавиатуру существующего сообщения
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Страница {page}:\n\n{text}",
            reply_markup=paginator.markup
        )
    else:
        # Отправляем новое сообщение с текстом и клавиатурой для пагинации
        bot.send_message(
            chat_id,
            text=f"Страница {page}:\n\n{text}",
            reply_markup=paginator.markup
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('page#'))
def callback_page_handler(call):
    user_id = call.from_user.id

    # Получаем номер страницы из данных кнопки
    page = int(call.data.split('#')[1])

    # Извлекаем ранее отсортированные фильмы из словаря
    sorted_movies = user_movies.get(user_id, [])

    if not sorted_movies:
        bot.send_message(
            call.message.chat.id,
            "Не удалось найти результаты для данной страницы."
        )
        return

    # Обновляем сообщение с новой страницей
    send_paginated_message(call.message.chat.id, sorted_movies, page, message_id=call.message.message_id)


def initiate_budget_search(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Выберите бюджет фильмов для отображения",
        reply_markup=gen_budget(),
    )
    bot.set_state(message.from_user.id, MyState.state_budget, message.chat.id)


# Глобальный словарь для хранения отсортированных фильмов по бюджету для каждого пользователя
user_budget_movies = {}

def initiate_budget_search(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Выберите бюджет фильмов для отображения",
        reply_markup=gen_budget(),  # Генерация клавиатуры для выбора бюджета
    )
    bot.set_state(message.from_user.id, MyState.state_budget, message.chat.id)


@bot.message_handler(commands=["budget"])
def handle_budget_command(message):
    initiate_budget_search(message)


@bot.message_handler(func=lambda message: message.text == "Найти фильм по бюджету")
def handle_budget_text(message):
    initiate_budget_search(message)


@bot.callback_query_handler(func=lambda callback_query: callback_query.data in ["low_budget_sort", "high_budget_sort"])
def sort_budget_movies(callback_query):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    # Удаляем клавиатуру
    bot.edit_message_reply_markup(chat_id, callback_query.message.message_id)

    # Определяем, какой тип бюджета выбран
    request_value = "Поиск фильмов по низкому бюджету" if callback_query.data == "low_budget_sort" else "Поиск фильмов по высокому бюджету"

    # Сохраняем запрос в базе данных
    RequestStorage.create(
        user_id=user_id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=request_value
    )

    # Получаем список фильмов по бюджету и сохраняем в глобальном словаре
    movie_list = movie_by_budget.movie_budget(callback_query.data)
    user_budget_movies[user_id] = movie_list

    if not movie_list:
        bot.send_message(
            chat_id,
            "К сожалению, не удалось найти фильмы с таким бюджетом"
        )
    else:
        # Отправляем первую страницу с результатами
        send_paginated_budget_message(chat_id, movie_list, 1)

    bot.delete_state(user_id, chat_id)


def send_paginated_budget_message(chat_id, movie_list, page, message_id=None):
    items = len(movie_list)
    items_per_page = 1
    total_pages = (items // items_per_page) + (1 if items % items_per_page > 0 else 0)

    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=page,
        data_pattern='budget_page#{page}'
    )

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_items = movie_list[start:end]

    text = "\n".join(map(str, page_items))

    if message_id:
        # Обновляем текст и клавиатуру существующего сообщения
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Страница {page}:\n\n{text}",
            reply_markup=paginator.markup
        )
    else:
        # Отправляем новое сообщение с текстом и клавиатурой для пагинации
        bot.send_message(
            chat_id,
            text=f"Страница {page}:\n\n{text}",
            reply_markup=paginator.markup
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('budget_page#'))
def callback_budget_page_handler(call):
    user_id = call.from_user.id

    # Получаем номер страницы из данных кнопки
    page = int(call.data.split('#')[1])

    # Извлекаем ранее отсортированные фильмы из словаря
    sorted_budget_movies = user_budget_movies.get(user_id, [])

    if not sorted_budget_movies:
        bot.send_message(
            call.message.chat.id,
            "Не удалось найти результаты для данной страницы."
        )
        return

    # Обновляем сообщение с новой страницей
    send_paginated_budget_message(call.message.chat.id, sorted_budget_movies, page, message_id=call.message.message_id)

@bot.message_handler(commands=["history"])
def search_by_history(message):
    query = (RequestStorage
             .select(RequestStorage.date_r, RequestStorage.request_value)
             .where(RequestStorage.user_id == message.chat.id)
             .order_by(RequestStorage.date_r.desc())
             .limit(5)
             )
    if query.exists():
        history = "Ваши последние 5 запросов:\n"
        history += "\n".join([f"{record.date_r}: {record.request_value}" for record in query])
    else:
        history = "История запросов пуста."
    bot.send_message(
        message.from_user.id,
        history
    )


@bot.message_handler(commands=['help'])
def faq_help(message):
    command_list = "Список доступных команд:"
    for k, v in command_dict.items():
        command_list += f"\n/{k}: {v}"
    bot.send_message(
        message.from_user.id,
        command_list
    )
