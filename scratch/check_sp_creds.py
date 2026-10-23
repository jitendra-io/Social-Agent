import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
nodes_json = cur.execute("SELECT nodes FROM workflow_entity WHERE id = 'fk5xv1XIQgn8rgwB'").fetchone()[0]
nodes = json.loads(nodes_json)

for n in nodes:
    print(f"Node: {n['name']} ({n['id']}) -> Credentials: {n.get('credentials')}")
