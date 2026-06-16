import sqlite3

con_conn = sqlite3.connect("contact.db", check_same_thread=False)
con_cur = con_conn.cursor()
con_cur.execute("""
    CREATE TABLE IF NOT EXISTS contact
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar,
        age INTEGER,
        email varchar,
        city varchar
    )
""")
con_conn.commit()

feed_conn = sqlite3.connect("feedback.db", check_same_thread=False)
feed_cur = feed_conn.cursor()
feed_cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar,
        message varchar
    )
""")
feed_conn.commit()