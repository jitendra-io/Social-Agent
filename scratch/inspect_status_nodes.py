import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])
for n in nodes:
    if n.get('name') in ['Command Router', 'Query System Status', 'Send Status Response']:
        print(json.dumps(n, indent=2))
