import os
import telebot
from peewee import SqliteDatabase
from config import db_path


sqlite_db = SqliteDatabase(db_path, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})