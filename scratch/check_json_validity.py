import sqlite3
import json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

row = cur.execute("SELECT nodes, connections, settings FROM workflow_entity WHERE id = 'IGComBotWf9921XYZ'").fetchone()

for name, val in [("nodes", row[0]), ("connections", row[1]), ("settings", row[2])]:
    try:
        json.loads(val)
        print(f"{name}: Valid JSON")
    except Exception as e:
        print(f"{name}: INVALID JSON -> {e}")
        # print around the error position
        import re
        m = re.search(r'position (\d+)', str(e))
        if m:
            pos = int(m.group(1))
            start = max(0, pos - 40)
            end = min(len(val), pos + 40)
            print(f"Snippet at {pos}: {repr(val[start:end])}")
