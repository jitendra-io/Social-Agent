import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

print("--- OUTBOX ---")
for r in cur.execute("SELECT * FROM workflow_publication_outbox").fetchall():
    print(r)

print("\n--- RETRY STATE ---")
for r in cur.execute("SELECT * FROM workflow_publication_retry_state").fetchall():
    print(r)

print("\n--- TRIGGER STATUS for RrAQsjiXlHhEcLNT ---")
for r in cur.execute("SELECT * FROM workflow_publication_trigger_status WHERE workflowId = 'RrAQsjiXlHhEcLNT'").fetchall():
    print(r)
