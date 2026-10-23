import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT connections FROM workflow_history WHERE versionId='bfcd1622-ddb3-4b41-a1d2-200c59f279ef'").fetchone()
conns = json.loads(row[0])
print("Connections in workflow_history:")
for src, targets in conns.items():
    print(f"  {src} -> {targets}")
