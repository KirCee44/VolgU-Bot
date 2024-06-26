import sqlite3

names_group = ['сак-212', 'сак-211']

#Функция проверки регистрации
def chack_registration(id):
    check = False
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    id_user = cursor.execute("SELECT id FROM users;")
    id_user = id_user.fetchall()
    id_user=' '.join(map(str, id_user))
    if str(id) in id_user:
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
    
    def is_valid(self):
        check_valid = False
        if self.name_group.lower() in names_group:
            check_valid = True
        return check_valid
            
    
    def registration(self):
        connect = sqlite3.connect('user.db')
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users (user, id, group_name, password, email) VALUES (?, ?, ?, ?, ?);", (self.name, self.id, self.name_group, self.password, self.email))
        cursor.close()
        connect.commit()
        
def information_user(id):
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    information = cursor.execute("SELECT group_name FROM users WHERE id = ?", (id,))
    information = information.fetchall()[0][0]
    cursor.close()
    connect.commit()
    return information.lower()