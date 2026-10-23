import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])
tg_node = [n for n in nodes if n.get('type') == 'n8n-nodes-base.telegramTrigger'][0]
print(json.dumps(tg_node, indent=2))
