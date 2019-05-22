import os
import telebot
from telebot import types
from telebot.types import Message
import cv2
from invert import apply_invert
import run_face_swap
from run_face_swap import face_swap
import requests

TOKEN = '895248757:AAH7tjGZjkiRSyAOCInlSn4F0auuaqD55XE'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я Bot the Face Swapper! Пришли мне свою фотку.')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Сейчас я могу:\n''/meme - прислать свой любимый мем :)\n')


@bot.message_handler(commands=['meme'])
def send_meme(message):
    # meme = open('sonic.png', 'rb')

    with open('sonic.png', 'rb') as meme:
        bot.send_photo(message.chat.id, meme)


@bot.message_handler(commands=['invert'])
def start_invert(message):
    msg = bot.send_message(message.chat.id, 'Хорошо. Пришли мне фотку :)')
    bot.register_next_step_handler(msg, send_invert)


def send_invert(message):
    if bot.message_handler(content_types=['photo']):
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open("photos/inving" + str(message.message_id) + ".jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            apply_invert("photos/inving" + str(message.message_id) + ".jpg", message)
            result = "photos/inved" + str(message.message_id) + ".jpg"
            bot.send_photo(message.chat.id, (open(result, "rb")))
            os.remove("photos/inving" + str(message.message_id) + ".jpg")
            os.remove(result)
        except Exception as e:
            bot.send_message(message.chat.id, e)
    else:
        bot.send_message(message.chat.id, "Что-то я не понял...")


@bot.message_handler(content_types=['photo'])
def handle_face_swap(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("photos/swapping" + str(message.message_id) + ".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        face_swap("photos/swapping" + str(message.message_id) + ".jpg", message)
        result = "photos/swapped" + str(message.message_id) + ".jpg"
        bot.send_photo(message.chat.id, (open(result, "rb")))
        os.remove("photos/swapping" + str(message.message_id) + ".jpg")
        os.remove(result)
    except Exception as e:
        bot.send_message(message.chat.id, e)

    #     file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    #     downloaded_file = bot.download_file(file_info.file_path)
    #
    #     with open("photos/new_file.jpg", 'wb') as new_file:
    #         new_file.write(downloaded_file)
    #     bot.send_message(message.chat.id, "Фото добавлено")
    # except Exception as e:
    #     bot.send_message(message.chat.id, e)


@bot.message_handler(func=lambda message: True)
def send_dialog(message: Message):
    bot.send_message(message.chat.id, 'Салют!')


bot.polling(interval=0, timeout=10)
