import telebot
from telebot import types
from config import token, link_generation
import registration.registration as registration
import database.database as database
import datetime
from config import media
from schedule import schedule, numerator_denominator

token = token.token

check_registration = False

#Создание клавиатуры кнопок для функции обновления рассписания
keydoard_choise_day_in_week = types.InlineKeyboardMarkup()
choise_day_in_week_button = [
    types.InlineKeyboardButton("Понедельник", callback_data='0'),
    types.InlineKeyboardButton("Вторник", callback_data='1'),
    types.InlineKeyboardButton("Среда", callback_data='2'), types.InlineKeyboardButton("Четверг",callback_data='3'),
    types.InlineKeyboardButton("Пятница", callback_data='4'),
    types.InlineKeyboardButton("Суббота", callback_data='5')
]
keydoard_choise_day_in_week.row(choise_day_in_week_button[0], choise_day_in_week_button[1], choise_day_in_week_button[2])
keydoard_choise_day_in_week.row(choise_day_in_week_button[3], choise_day_in_week_button[4], choise_day_in_week_button[5])

#Список дней недели и числитель знаменатель, а также переменная числитель и знаменатель которая содержит функцию расчета числителя знаменателя
week_day = ['понедельник','вторник','среда','четверг','пятница','субботу', 'воскресенье']
numerator_and_denominator_text = ['числитель', 'знаменатель']
numerator_and_denominator = numerator_denominator.numerator_denominator()

#Дата
date = datetime.date.today()

bot = telebot.TeleBot(token)

#Функция отвечающая на команду /start
@bot.message_handler(commands=['start'])
def start(message):
    global check_registration
    info_registration = 'Вы зарегистрированны'

    #Создание экранной клавиатуры
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    couples = types.KeyboardButton('Расписание пар')
    time = types.KeyboardButton('Расписание пар по времени')
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

#Обработчик команды /reg
@bot.message_handler(commands=['reg'])
def registration_in_bot(message):
    user_input_cache = message.text.split()
    user_information = {
        'user_id': message.from_user.id,
        'user_name': message.from_user.first_name,
        'group_name': user_input_cache[1],
        'password': user_input_cache[2],
        'email': user_input_cache[-1],
    }

    #Выполнение функции регистрации
    registration_output = registration.Registration(
        user_information['user_id'],
        user_information['user_name'],
        user_information['group_name'],
        user_information['password'],
        user_information['email']
        )
    if registration_output.is_valid():
        registration_output.registration()
        bot.send_message(message.chat.id, 'Вы зарегистрированны')
    else:
        bot.send_message(message.chat.id, 'Вы ввели не существующую группу')

#Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def input_user_information(call):
    number_day = date.weekday()

    #Выводит подсказку к регистрации при нажатии на кнопку "Зарегистрироваться"
    if call.data == 'registration':
        bot.send_message(call.message.chat.id, "Введите данный о себе по примеру: /reg САк-212 *пароль* SAk-212_123456789@volsu.ru)\n(данные от личного кабинета не обязательны, если вы не хотите их вводить, то вместо этого введите нули)")

    #Обновление сообщения расписания
    number_day = int(call.data)
    save_url = link_generation.link_generation(media.media, registration.information_user(call.message.chat.id), f'week_{numerator_and_denominator}\image.jpg')
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_photo(
        chat_id= call.message.chat.id,
        photo= open(schedule.geniration_schedule_image(media.schedule_template, save_url, number_day, f'{media.media}/{registration.information_user(call.message.chat.id)}/week_{numerator_and_denominator}/week.txt'), 'rb'),
        caption= f"<b>День недели:</b> {week_day[number_day]}\n<b>Неделя:</b> {numerator_and_denominator_text[numerator_and_denominator]}\n<b>Группа:</b> {registration.information_user(call.message.chat.id)}",
        reply_markup= keydoard_choise_day_in_week, parse_mode= "html"
    )

#Оброботчик текстовых запросов
@bot.message_handler(content_types=['text'])
def handler_imput_text(message):
    #Вывод информации о профиле
    if message.text == 'Профиль':
        message_keyboard = types.InlineKeyboardMarkup()
        registration_button = types.InlineKeyboardButton('Зарегистрироваться', callback_data='registration')
        user_information_profile = {
            'status':'вы не зарегистрированны',
            'user_id':message.from_user.id,
            'name':message.from_user.first_name,
            'group_name':'*'
        }

        if registration.chack_registration(int(user_information_profile['user_id'])) == True:
            user_information_profile['status'] = 'вы зарегистрированны'
            user_information_profile['group_name'] = registration.information_user(user_information_profile['user_id'])
        elif registration.chack_registration(int(user_information_profile['user_id'])) == False:
            message_keyboard.add(registration_button)
            user_information_profile['group_name'] = '*'

        bot.send_message(message.chat.id,f"<b>├ ID:</b> {user_information_profile['user_id']}\n<b>├ Имя:</b> {user_information_profile['name']}\n<b>├ Группа:</b> {user_information_profile['group_name']}\n<b>├ Статус:</b> {user_information_profile['status']}",reply_markup=message_keyboard, parse_mode='html')

    #Выводит расписание по времени
    elif message.text == 'Расписание пар по времени':
        bot.send_photo(message.chat.id, open(media.pairing_schedule, 'rb'), caption="<b>Расписание пар по времени</b>", parse_mode='html')
        
    #Выводит сгенирированное расписание пар
    if registration.chack_registration(message.from_user.id) == True:
        if message.text == 'Расписание пар':
            save_url = link_generation.link_generation(media.media, registration.information_user(message.from_user.id), f'week_{numerator_and_denominator}/image.jpg')
            bot.send_photo(message.chat.id,open(schedule.geniration_schedule_image(media.schedule_template, save_url, date.weekday(), f'{media.media}/{registration.information_user(message.from_user.id)}/week_{numerator_and_denominator}/week.txt'), 'rb'),caption=f"<b>День недели:</b> {week_day[date.weekday()]}\n<b>Неделя:</b> {numerator_and_denominator_text[numerator_and_denominator]}\n<b>Группа:</b> {registration.information_user(message.from_user.id)}",reply_markup=keydoard_choise_day_in_week, parse_mode="html")
    else:
        if message.text == 'Расписание пар':
            bot.send_message(message.chat.id, 'Вы не зарегистрированны')
    
bot.infinity_polling()