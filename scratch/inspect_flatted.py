import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
data_str = cur.execute("SELECT data FROM execution_data WHERE executionId = 73").fetchone()[0]
data = json.loads(data_str)

for idx, item in enumerate(data[:35]):
    print(f"[{idx}]: {item}")
