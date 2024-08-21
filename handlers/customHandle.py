from datetime import datetime

from peewee import IntegrityError
from telebot.custom_filters import StateFilter
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from keyboards.key import *
from config import bot
from database.models import RequestStorage, Users
from states.mainState import MyState
from api import movie_by_name

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




@bot.message_handler(func=lambda message: message.text == "Найти фильм по названию")
def search_by_name(message):
    bot.send_message(
        message.from_user.id,
        "Введите название фильма",
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler()
def push_res(message):
    RequestStorage.create(
        user_id=message.from_user.id,
        date_r=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_value=f"Поиск фильма: {message.text}"
    )

    bot.send_message(
        message.from_user.id,
        movie_by_name.search_film(message.text)
    )


# @bot.message_handler(commands=["button_name"])
# @bot.message_handler(func=lambda message: message.text == "Найти фильм по названию")
# def search_by_name(message):
#     bot.set_state(message.from_user.id, MyState.state_one)
#     bot.send_message(
#         message.from_user.id,
#         "Введите название фильма"
#     )


# @bot.message_handler(commands=["button_rating"])
# @bot.message_handler(commands=["button_budget"])
# @bot.message_handler(commands=["button_history"])

