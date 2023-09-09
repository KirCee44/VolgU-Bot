import sqlite3

db = sqlite3.connect('user.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXIST users(
    user TEXT,
    id INTAGER,
    group TEXT,
    password TEXT,
    email TEXT,)
""")

db.commit()