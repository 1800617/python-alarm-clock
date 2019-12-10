import sqlite3

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

c.execute('''CREATE TABLE alarms (id integer PRIMARY KEY AUTOINCREMENT,time text NOT NULL)''')

c.execute("INSERT INTO alarms (time) VALUES ('07:15')")
c.execute("INSERT INTO alarms (time) VALUES ('09:30')")
c.execute("INSERT INTO alarms (time) VALUES ('11:30')")

conn.commit()

conn.close()