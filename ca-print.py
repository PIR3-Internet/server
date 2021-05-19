import sqlite3

con = sqlite3.connect('ca-providers.db')
cur = con.cursor()

cur.execute("select * from ca")
print(cur.fetchall())

con.close()