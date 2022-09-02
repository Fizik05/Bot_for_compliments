import os

import requests

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          MessageHandler,
                          Filters,
                          CommandHandler)
from deep_translator import GoogleTranslator


load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)
URL = "https://complimentr.com/api"

def get_new_compliment():
    """Эта функция отправляет комплименты"""
    response = requests.get(URL).json()
    random_compliment = str(response.get("compliment"))
    result = GoogleTranslator(
        source="auto",
        target="ru",
    ).translate(random_compliment)
    return result

def new_compliment(update, context):
    """Эта функция обрабатывает команду /newcompliment"""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text=get_new_compliment())

def wake_up(update, context):
    """Эта фунция обрабатывает команду /start"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([["/newcompliment"]], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text="Привет, {}".format(name),
        reply_markup=button
    )

    context.bot.send_message(chat_id=chat.id,
                             text=get_new_compliment())

def for_errors(update, contex):
    """Эта функция для обработки неопределённых команд"""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)

    contex.bot.send_message(
        chat_id=chat.id,
        text=f"К сожалению, я не смог распознать твою команду:(\nПопробуй команду ниже;)",
        reply_markup=button
    )


def main():
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("newcompliment", new_compliment))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, for_errors))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
