from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_start():
    # Создаем объекты кнопок
    button_name = KeyboardButton(text="Найти фильм по названию")
    button_budget = KeyboardButton(text="Найти фильм по бюджету")
    button_rating = KeyboardButton(text="Найти фильм по рейтингу")
    button_history = KeyboardButton(text="Посмотреть историю запросов")

    # Создаем объект клавиатуры
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        button_name,
        button_rating,
        button_budget,
        button_history
    )
    return keyboard


