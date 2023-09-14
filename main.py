import telebot
from telebot import types
from config import token, media
import registration.registration as registration
import database.database as database
import datetime


token = token.token

check_registration = False

keydoard_choise_day_in_week = types.InlineKeyboardMarkup()
choise_day_in_week_button = [types.InlineKeyboardButton("Понедельник", callback_data='0'), types.InlineKeyboardButton("Вторник", callback_data='1'), types.InlineKeyboardButton("Среда", callback_data='2'), types.InlineKeyboardButton("Четверг", callback_data='3'), types.InlineKeyboardButton("Пятница", callback_data='4'), types.InlineKeyboardButton("Суббота", callback_data='5')]
keydoard_choise_day_in_week.add(choise_day_in_week_button[0], choise_day_in_week_button[1], choise_day_in_week_button[2], choise_day_in_week_button[3], choise_day_in_week_button[4], choise_day_in_week_button[5])

week_day = ['понедельник','вторник','среду','четверг','пятницу','субботу', 'воскресенье']
date = datetime.date.today() 

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
    number_day = date.weekday()
    if call.data == 'registration':
        bot.send_message(call.message.chat.id, 'Введите данный о себе по примеру: /reg название и номер группы, пароль от личного кабинета и электронную почту на которую зерегистрирован личный кабинет(Например: /reg САк-212 *пароль* SAk-212_123456789@volsu.ru) (данные от личного кабинета не обязательны, если вы не хотите их вводить, то вместо этого введите нули)')
    elif call.data == '0':
        number_day = 0
    elif call.data == '1':
        number_day = 1
    elif call.data == '2':
        number_day = 2
    elif call.data == '3':
        number_day = 3
    elif call.data == '4':
        number_day = 4
    elif call.data == '5':
        number_day = 5
    bot.edit_message_media(media = telebot.types.InputMedia(type = 'photo', media = open(media.schedule_on_day[0][number_day], 'rb')), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keydoard_choise_day_in_week)		

@bot.message_handler(content_types=['text'])
def handler_imput_text(message):
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
    elif message.text == 'Рассписание пар по времени':
        bot.send_photo(message.chat.id, open(media.pairing_schedule, 'rb'), caption="Расписание пар по времени")
    elif message.text == 'Рассписание пар':
        bot.send_photo(message.chat.id, open(media.schedule_on_day[0][date.weekday()], 'rb'), caption=f"Расписание пар на {week_day[date.weekday()]}", reply_markup=keydoard_choise_day_in_week)
        
bot.infinity_polling()