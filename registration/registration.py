import sqlite3

#Функция проверки регистрации
def chack_registration(id):
    check = False
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    id_user = cursor.execute("SELECT id FROM users")
    id_user = id_user.fetchall()
    if id_user:
        id_user = id_user[0]
    if id in id_user:
        check = True
    connect.commit()
    return check

class Registration:
    def __init__(self, id, name: str, name_group: str, password: str, email: str) -> None:
        self.id = id
        self.name = name
        self.name_group = name_group
        self.password = password
        self.email = email
        
    def registration(self):
        connect = sqlite3.connect('user.db')
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users (user, id, group_name, password, email) VALUES (?, ?, ?, ?, ?);", (self.name, self.id, self.name_group, self.password, self.email))
        cursor.close()
        connect.commit()