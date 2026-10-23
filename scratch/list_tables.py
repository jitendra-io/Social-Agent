import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("All tables:", tables)
