import os
import telebot
from dotenv import load_dotenv
from peewee import SqliteDatabase

# Загружаем файл .env
load_dotenv()

# активируем токен для работы с ботом
bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))

# SQLite database using WAL journal mode and 64MB cache.
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'database', 'database.db')
