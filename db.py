import sqlite3

con = sqlite3.connect('subscriptions.db')
cur = con.cursor()
cur.execute("""CREATE TABLE "videos" (
	"title"	TEXT,
	"url"	TEXT,
	"desc" TEXT )""")