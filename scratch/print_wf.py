import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes, connections FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])
conns = json.loads(row[1])

print("Node names:", [n['name'] for n in nodes])
print("Connections:")
for src, targets in conns.items():
    print(f"  {src} -> {targets}")
