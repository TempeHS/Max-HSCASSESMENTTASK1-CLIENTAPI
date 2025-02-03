import sqlite3 as sql

database = ".databaseFiles/database.db"

def new_entry(devtag, project, repo, starttime, endtime):
    try:
        con = sql.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO entries (devtag, project, repo, starttime, endtime) VALUES (?, ?, ?, ?, ?)", (devtag, project, repo, starttime, endtime))
        con.commit()
        con.close()
        return True
    except sql.Error as e:
        print(f"An error occurred: {e}")

def entries():
    con = sql.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM entries")
    entries = cur.fetchall()
    con.close()
    return entries