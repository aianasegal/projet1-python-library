import sqlite3
con = sqlite3.connect("books.db")
cur = con.cursor()
SQL= "ALTER TABLE book ADD COLUMN county VARCHAR(100)"




cur.execute(SQL)





