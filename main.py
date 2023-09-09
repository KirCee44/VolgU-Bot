import telebot
from telebot import types
from config import token

token = token.token

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    couples = types.KeyboardButton('Рассписание пар')
    time = types.KeyboardButton('Рассписание пар по времени')
    profile = types.KeyboardButton('Профиль')
    information = types.KeyboardButton('Информация')
    keyboard.row(couples)
    keyboard.row(time, information)
    keyboard.row(profile)
    bot.send_message(message.chat.id, f'Добрый день, {message.from_user.first_name}', reply_markup=keyboard)

bot.infinity_polling()