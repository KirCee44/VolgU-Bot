import sqlite3

#Подключение к базе данных
db = sqlite3.connect('user.db')
cursor = db.cursor()

#Создание базы данных
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user TEXT,
    id INTAGER,
    group_name TEXT,
    password TEXT,
    email TEXT);
""")

db.commit()