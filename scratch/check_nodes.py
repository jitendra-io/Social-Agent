import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])
for n in nodes:
    ntype = n.get('type', '')
    if 'mySql' in ntype or 'telegram' in ntype:
        print(f"{n.get('name')} ({ntype}): credentials={n.get('credentials')}")
