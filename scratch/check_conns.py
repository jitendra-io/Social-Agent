import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT connections FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
conns = json.loads(row[0])
print("Command Router connections in DB:")
print(json.dumps(conns.get('Command Router'), indent=2))
