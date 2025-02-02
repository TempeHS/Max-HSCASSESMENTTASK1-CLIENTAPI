import sqlite3 as sql
import bcrypt

def create_table():
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            devtag TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def addUser(devtag, password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        con = sql.connect(".databaseFiles/database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (devtag, password) VALUES (?, ?)", (devtag, hashed))
        con.commit()
        con.close()
        return True
    except sql.IntegrityError:
        return False 

def checkUser(devtag, password):
    con = sql.connect(".databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE devtag=?", (devtag,))
    result = cur.fetchone()
    con.close()
    if result and bcrypt.checkpw(password.encode("utf-8"), result[0]):
        return True
    return False


create_table()
