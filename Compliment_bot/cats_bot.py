import os

import requests

from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          MessageHandler,
                          Filters,
                          CommandHandler)


load_dotenv()

token = os.getenv("Token")
updater = Updater(token=token)
URL = "https://api.thecatapi.com/v1/images/search"

def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([["/newcat"]], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text="Привет, {}. Посмотри, какого котика я тебе нашёл.".format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())
    
    
def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    updater.start_polling(poll_interval=15.0)
    updater.idle()


if __name__ == "__main__":
    main()
