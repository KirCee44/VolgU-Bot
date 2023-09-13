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
    global check_registration
    info_registration = 'Вы зарегистрированны'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    couples = types.KeyboardButton('Рассписание пар')
    time = types.KeyboardButton('Рассписание пар по времени')
    profile = types.KeyboardButton('Профиль')
    information = types.KeyboardButton('Информация')
    keyboard.row(couples)
    keyboard.row(time, information)
    keyboard.row(profile)
    
    if registration.chack_registration(message.from_user.id):
        check_registration = True
    if check_registration == False:
        info_registration = 'Вы не зарегистрированны'
     
    bot.send_message(message.chat.id, f'Добрый день, {message.from_user.first_name}. {info_registration}', reply_markup=keyboard)
    
@bot.message_handler(commands=['reg'])
def registration_in_bot(message):
    user_input_cache = message.text.split()
    user_information = {
        'user_id': message.from_user.id,
        'user_name': message.from_user.first_name[0],
        'group_name': user_input_cache[1],
        'password': user_input_cache[2],
        'email': user_input_cache[-1],
    }
    registration_output = registration.Registration(id=user_information['user_id'], name=user_information['user_name'], name_group=user_information['group_name'], password=user_information['password'], email=user_information['email'])
    registration_output.registration()
    bot.send_message(message.chat.id, 'Вы зарегистрированны')

@bot.callback_query_handler(func=lambda call: True)
def input_user_information(call):
    if call.data == 'registration':
        bot.send_message(call.message.chat.id, 'Введите данный о себе по примеру: /reg название и номер группы, пароль от личного кабинета и электронную почту на которую зерегистрирован личный кабинет(Например: /reg САк-212 *пароль* SAk-212_#########@volsu.ru) (данные от личного кабинета не обязательные, если вы не хотите вводить данные о личном кабинете, то вместо них впешите нули)')
    
@bot.message_handler(content_types=['text'])
def profile(message):
    if message.text == 'Профиль':
        message_keyboard = types.InlineKeyboardMarkup()
        registration_button = types.InlineKeyboardButton('Зарегистрироваться', callback_data='registration')
        status = 'вы не зарегистрированны'
        user_id = message.from_user.id
        name = message.from_user.first_name
        group_name = '*'
        if registration.chack_registration(user_id):
            status = 'вы зарегистрированны'
        else:
            message_keyboard.add(registration_button)
        bot.send_message(message.chat.id, f"""<b>├ ID:</b> {user_id}\n<b>├ Имя:</b> {name}\n<b>├ Группа:</b> {group_name}\n<b>├ Статус:</b> {status}""", parse_mode='html', reply_markup=message_keyboard)     

bot.infinity_polling()