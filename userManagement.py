import sqlite3 as sql
import bcrypt
import bleach
from flask import request
from datetime import timedelta

database = ".databaseFiles/database.db"
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=15)

def addUser(devtag, password):
    devtag = bleach.clean(devtag.strip())
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        con = sql.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO users (devtag, password) VALUES (?, ?)", (devtag, hashed))
        con.commit()
        return True
    except sql.IntegrityError:
        return False
    finally:
        con.close()

def checkUser(devtag, password):
    devtag = bleach.clean(devtag.strip())

    con = sql.connect(database)
    cur = con.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM failed_logins WHERE devtag = ? AND timestamp > datetime('now', '-15 minutes')
    """, (devtag,))
    failed_attempts = cur.fetchone()[0]

    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        con.close()
        return "locked"

    cur.execute("SELECT password FROM users WHERE devtag=?", (devtag,))
    result = cur.fetchone()

    if result and bcrypt.checkpw(password.encode("utf-8"), result[0]):
        return True

    cur.execute("INSERT INTO failed_logins (devtag, ip_address) VALUES (?, ?)", (devtag, request.remote_addr))
    con.commit()
    return False