import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes, connections FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])
conns = json.loads(row[1])

cr_conns = conns.get('Command Router')
print("Command Router connections:")
print(json.dumps(cr_conns, indent=2))

for n in nodes:
    if n['name'] in ['Command Router', 'Query System Status']:
        print("Node:", n['name'])
        print(json.dumps(n, indent=2))
