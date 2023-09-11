import sqlite3

#Функция проверки регистрации
def chack_registration(id):
    check = False
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    id_user = cursor.execute("SELECT id FROM users")
    if id in id_user:
        check = True
    connect.commit()
    return check

