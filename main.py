import telebot
from telebot import types
from config import token
import registration.registration as registration
import database.database as database

token = token.token

check_registration = False

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    info_registration = 'Вы зарегистрированны'
    
    keyboard = types.ReplyKeyboardMarkup()
    couples = types.KeyboardButton('Рассписание пар')
    time = types.KeyboardButton('Рассписание пар по времени')
    profile = types.KeyboardButton('Профиль')
    information = types.KeyboardButton('Информация')
    keyboard.row(couples)
    keyboard.row(time, information)
    keyboard.row(profile)
    
    if registration.chack_registration(message.from_user.id) == True:
        check_registration = True
        if not check_registration:
            info_registration = 'Вы не зарегистрированны'
    bot.send_message(message.chat.id, f'Добрый день, {message.from_user.first_name}. {info_registration}', reply_markup=keyboard)

bot.infinity_polling()