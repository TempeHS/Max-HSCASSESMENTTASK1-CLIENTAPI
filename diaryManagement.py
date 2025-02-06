import sqlite3 as sql
import bleach
import os

database = os.path.join(os.path.dirname(__file__), ".databaseFiles/database.db")

def new_entry(devtag, project, repo, starttime, endtime):
    devtag, project, repo, starttime, endtime = map(bleach.clean, [devtag, project, repo, starttime, endtime])
    con = sql.connect(database)
    cur = con.cursor()
    cur.execute("INSERT INTO entries (devtag, project, repo, starttime, endtime) VALUES (?, ?, ?, ?, ?)",
                (devtag, project, repo, starttime, endtime))
    con.commit()
    con.close()

def entries():
    try:
        con = sql.connect(database)
        cur = con.cursor()
        cur.execute("SELECT * FROM entries")
        diary_entries = cur.fetchall()
        return diary_entries
    except sql.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        con.close()