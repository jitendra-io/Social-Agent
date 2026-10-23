import sqlite3
import datetime

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%f')[:-3]

# 1. Clear outbox entries and retry state for IGComBotWf9921XYZ
cur.execute("DELETE FROM workflow_publication_retry_state WHERE workflowId = 'IGComBotWf9921XYZ'")
cur.execute("DELETE FROM workflow_publication_outbox WHERE workflowId = 'IGComBotWf9921XYZ'")

# 2. Insert fresh pending publication
cur.execute("""
INSERT INTO workflow_publication_outbox (workflowId, publishedVersionId, status, reason, errorMessage, createdAt, updatedAt)
VALUES ('IGComBotWf9921XYZ', 'dc18f98a-4852-42c0-96b9-357add8786e3', 'pending', 'publish', NULL, ?, ?)
""", (now, now))

con.commit()
print("Outbox updated with pending publication.")

for r in cur.execute("SELECT * FROM workflow_publication_outbox WHERE workflowId = 'IGComBotWf9921XYZ'").fetchall():
    print("Outbox row:", r)

con.close()
