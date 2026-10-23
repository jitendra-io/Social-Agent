import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_history WHERE versionId='bfcd1622-ddb3-4b41-a1d2-200c59f279ef'").fetchone()
nodes = json.loads(row[0])
n = [x for x in nodes if x['name'] == 'Query System Status'][0]
print("Query System Status in workflow_history:")
print(json.dumps(n, indent=2))
