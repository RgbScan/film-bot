from datetime import datetime

from peewee import IntegrityError
from telebot.custom_filters import StateFilter


from keyboards.key import *
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


# Команда для поиска фильма по названию
@bot.message_handler(commands=["start, button_name"])
@bot.message_handler(func=lambda message: message.text == "Найти фильм по названию")
def search_by_name(message):
    bot.send_message(
        message.from_user.id,
        "Введите название фильма",
        reply_markup=ReplyKeyboardRemove
    )
    bot.set_state(message.from_user.id, MyState.state_name, message.chat.id)


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


@bot.message_handler(commands=["button_rating"])
@bot.message_handler(func=lambda message: message.text == "Найти фильм по рейтингу")
def search_by_rating(message):
    bot.send_message(
        message.from_user.id,
        "Введите рейтинг фильмов для поиска."
        "Вы можете ввести одно значение, например: 5.5 или 8."
        "или можете ввести сразу несколько значений через запятую, например: 5, 6.5, 8, 7",
    )
    bot.set_state(message.from_user.id, MyState.state_rating, message.chat.id)


@bot.message_handler(state=MyState.state_rating)
def sort_max_to_min(message):
    RequestStorage.create(
        user_id=message.from_user.id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=f"Поиск фильмов по рейтингу: {message.text}"
    )
    bot.send_message(
        message.from_user.id,
        movie_by_rating.sort_rating(message.text),
    )
    bot.delete_state(message.from_user.id, message.chat.id)


# @bot.message_handler(commands=["button_budget"])
# def search_by_name(message):
#     bot.set_state(message.from_user.id, MyState.state_one)
#     bot.send_message(
#         message.from_user.id,
#         "Введите название фильма",
#     )
#
#
# @bot.message_handler(commands=["button_history"])
# def search_by_name(message):
#     bot.set_state(message.from_user.id, MyState.state_one)
#     bot.send_message(
#         message.from_user.id,
#         "Введите название фильма",
#     )







