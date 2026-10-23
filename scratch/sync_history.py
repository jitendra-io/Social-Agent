import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

# Update workflow_history so published runtime matches workflow_entity
rows = cur.execute("""
    SELECT w.activeVersionId, w.nodes, w.connections 
    FROM workflow_entity w 
    WHERE w.active = 1
""").fetchall()

for version_id, nodes, conns in rows:
    cur.execute("""
        UPDATE workflow_history 
        SET nodes = ?, connections = ? 
        WHERE versionId = ?
    """, (nodes, conns, version_id))
    print(f"Synced published version {version_id} in workflow_history!")

con.commit()
con.close()
print("All published snapshots successfully synced!")
