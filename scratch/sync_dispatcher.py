import sqlite3, json

with open('workflows/telegram_dispatcher.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

nodes_str = json.dumps(wf['nodes'])
conns_str = json.dumps(wf['connections'])

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (nodes_str, conns_str))
cur.execute("UPDATE workflow_history SET nodes = ?, connections = ? WHERE versionId = 'bfcd1622-ddb3-4b41-a1d2-200c59f279ef'", (nodes_str, conns_str))
con.commit()
con.close()
print("Updated telegram dispatcher in both database tables!")
