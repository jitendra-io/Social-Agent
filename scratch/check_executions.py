import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

print("--- EXECUTIONS ---")
rows = cur.execute("SELECT id, finished, mode, status, workflowId, startedAt, stoppedAt FROM execution_entity ORDER BY id DESC LIMIT 5").fetchall()
for r in rows:
    print(r)

if rows:
    last_id = rows[0][0]
    data = cur.execute("SELECT data FROM execution_data WHERE executionId = ?", (last_id,)).fetchone()
    if data:
        print(f"Data for execution {last_id}:", data[0][:500])
