import telebot
from telebot.types import Message

TOKEN = '895248757:AAH7tjGZjkiRSyAOCInlSn4F0auuaqD55XE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Салют!')

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, 'Салют!')

bot.send_message(260747339, 'привет из скрипта!')

bot.polling()