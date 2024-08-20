from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards import key
from config import bot


@bot.message_handler(commands=["create_markup"])


