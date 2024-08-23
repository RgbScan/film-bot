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


def gen_budget():
    button_low = InlineKeyboardButton(text="С низким бюджетом", callback_data="low_budget_sort")
    button_high = InlineKeyboardButton(text="С высоким бюджетом", callback_data="high_budget_sort")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_low, button_high)
    return keyboard
