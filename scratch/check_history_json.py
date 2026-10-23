import sqlite3
import json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

row = cur.execute("SELECT nodes, connections FROM workflow_history WHERE workflowId = 'IGComBotWf9921XYZ'").fetchone()

for name, val in [("history nodes", row[0]), ("history connections", row[1])]:
    try:
        json.loads(val)
        print(f"{name}: Valid JSON")
    except Exception as e:
        print(f"{name}: INVALID JSON -> {e}")
        import re
        m = re.search(r'position (\d+)', str(e))
        if m:
            pos = int(m.group(1))
            start = max(0, pos - 40)
            end = min(len(val), pos + 40)
            print(f"Snippet at {pos}: {repr(val[start:end])}")

# Let's inspect position 2113 in nodes
nodes = cur.execute("SELECT nodes FROM workflow_history WHERE workflowId = 'IGComBotWf9921XYZ'").fetchone()[0]
print(f"Length of nodes: {len(nodes)}")
for i in range(2100, min(len(nodes), 2130)):
    print(f"[{i}] {repr(nodes[i])} (code: {ord(nodes[i])})")
