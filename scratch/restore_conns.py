import sqlite3, json

with open('workflows/telegram_dispatcher.json', 'r', encoding='utf-8') as f:
    file_wf = json.load(f)

file_conns = file_wf['connections']

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

cur.execute("UPDATE workflow_entity SET connections = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (json.dumps(file_conns),))
con.commit()

# Verify
row = cur.execute("SELECT connections FROM workflow_entity WHERE id = 'Y6ResnEyOHxuJIdI'").fetchone()
saved_conns = json.loads(row[0])
print("Saved keys in connections:", list(saved_conns.keys()))
print("Command Router outputs connected:", len(saved_conns.get('Command Router', {}).get('main', [])))

con.close()
