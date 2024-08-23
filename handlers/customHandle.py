import time
from datetime import datetime

from peewee import IntegrityError
from telebot.custom_filters import StateFilter
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardRemove

from keyboards.key import gen_budget, gen_start
from config import bot
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
    print(message.from_user.id, message.chat.id)

# Команда для поиска фильма по названию
@bot.message_handler(commands=["button_name"])
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
        "Вы можете ввести одно значение, например: 5.5 или 8."
        "или можете ввести сразу несколько значений через запятую, например: 5, 6.5, 8, 7",
    )
    bot.set_state(message.from_user.id, MyState.state_rating, message.chat.id)


@bot.message_handler(commands=["button_rating"])
def handle_rating_command(message):
    initiate_rating_search(message)


@bot.message_handler(func=lambda message: message.text == "Найти фильм по рейтингу")
def handle_rating_text(message):
    initiate_rating_search(message)


@bot.message_handler(state=MyState.state_rating)
def sort_max_to_min(message):
    RequestStorage.create(
        user_id=message.from_user.id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=f"Поиск фильмов по рейтингу: {message.text}"
    )
    movie_list = movie_by_rating.sort_rating(message.text)
    if movie_list == 0:
        bot.send_message(
            message.from_user.id,
            "К сожалению не удалось найти фильмы с таким рейтингом"
        )
    else:
        for movie in movie_list:
            bot.send_message(
                message.from_user.id,
                movie
            )
    bot.delete_state(message.from_user.id, message.chat.id)


def initiate_budget_search(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Выберите бюджет фильмов для отображения",
        reply_markup=gen_budget(),
    )
    bot.set_state(message.from_user.id, MyState.state_budget, message.chat.id)


@bot.message_handler(commands=["button_budget"])
def handle_budget_command(message):
    initiate_budget_search(message)


@bot.message_handler(func=lambda message: message.text == "Найти фильм по бюджету")
def handle_budget_text(message):
    initiate_budget_search(message)


@bot.callback_query_handler(func=lambda callback_query: callback_query.data in ["low_budget_sort", "high_budget_sort"])
def sort_low(callback_query):
    # Удаляем клавиатуру
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )

    request_value = "Поиск фильмов по низкому бюджету" if callback_query.data == "low_budget_sort" else "Поиск фильмов по высокому бюджету"

    RequestStorage.create(
        user_id=callback_query.from_user.id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=request_value
    )
    movie_list = movie_by_budget.movie_budget(callback_query.data)
    for movie in movie_list:
        bot.send_message(
            callback_query.from_user.id,
            movie,
        )
    bot.delete_state(callback_query.from_user.id, callback_query.message.chat.id)


@bot.message_handler(commands=["button_history"])
def search_by_history(message):
    query = (RequestStorage
             .select(RequestStorage.date_r, RequestStorage.request_value)
             .where(RequestStorage.user_id == message.chat.id)
             .order_by(RequestStorage.date_r.desc())
             .limit(5)
             )
    if query.exists():
        history = "\n".join([f"{record.date_r}: {record.request_value}" for record in query])
    else:
        history = "История запросов пуста."
    bot.send_message(
        message.from_user.id,
        history
    )
