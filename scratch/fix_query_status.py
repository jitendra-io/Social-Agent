import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])

for n in nodes:
    if n.get('name') == 'Query System Status':
        old_q = n['parameters']['query']
        n['parameters']['query'] = "SELECT (SELECT COUNT(*) FROM posts) AS total_posts, (SELECT COUNT(*) FROM posts WHERE status='published') AS published_count, (SELECT COUNT(*) FROM executive_memory) AS memory_count;"
        print("Updated Query System Status query in DB!")

cur.execute("UPDATE workflow_entity SET nodes = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (json.dumps(nodes),))
con.commit()
con.close()
print("Committed update to database.sqlite successfully!")
