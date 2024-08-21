import telebot
from config import bot
import handlers.customHandle
import states.mainState

if __name__ == "__main__":
    bot.infinity_polling()