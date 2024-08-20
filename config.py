import os
import telebot
from dotenv import load_dotenv

# Загружаем файл .env
load_dotenv()

# активируем токен для работы с ботом
bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))
