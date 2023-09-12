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
    
@bot.callback_query_handler(func=lambda call: True)
def input_user_information(call):
    if call.data == 'registration':
        bot.send_message(call.message.chat.id, 'Введите данный о себе по примеру: /reg название_и_номер_групп пароль_от_личного_кабинета электронную_почту_на_которую_зерегистрирован_личный_кабинет (данные от личного кабинета не обязательные)')
    
@bot.message_handler(content_types=['text'])
def profile(message):
    if message.text == 'Профиль':
        message_keyboard = types.InlineKeyboardMarkup()
        registration_button = types.InlineKeyboardButton('Зарегистрироваться', callback_data='registration')
        message_keyboard.add(registration_button)
        status = 'вы не зарегистрированны'
        user_id = message.from_user.id
        name = message.from_user.first_name
        group_name = '*'
        if registration.chack_registration(user_id):
            status = 'вы зарегистрированны'
        bot.send_message(message.chat.id, f"""<b>├ID:</b> {user_id}\n<b>├Имя:</b> {name}\n<b>├Группа:</b> {group_name}\n<b>├Статус:</b> {status}""", parse_mode='html', reply_markup=message_keyboard)     

bot.infinity_polling()