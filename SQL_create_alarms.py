import sqlite3

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

c.execute('''CREATE TABLE alarms (id integer PRIMARY KEY AUTOINCREMENT,time text NOT NULL)''')

alarms = [('02:15'), ('02:30'), ('07:15'), ('12:34')]
c.execute("INSERT INTO alarms (time) VALUES ('07:15')")
c.execute("INSERT INTO alarms (time) VALUES ('09:30')")
c.execute("INSERT INTO alarms (time) VALUES ('10:50')")
c.execute("INSERT INTO alarms (time) VALUES ('12:34')")

conn.commit()

conn.close()