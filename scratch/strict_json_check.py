import sqlite3
import json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

row = cur.execute("""
SELECT nodes, connections, settings, staticData, pinData, meta, nodeGroups 
FROM workflow_entity WHERE id = 'IGComBotWf9921XYZ'
""").fetchone()

col_names = ['nodes', 'connections', 'settings', 'staticData', 'pinData', 'meta', 'nodeGroups']

for name, val in zip(col_names, row):
    if val is not None:
        try:
            # strict=True enforces no unescaped control characters in strings
            json.loads(val, strict=True)
            print(f"workflow_entity.{name}: VALID (length {len(val)})")
        except Exception as e:
            print(f"workflow_entity.{name}: ERROR -> {e}")
            import re
            m = re.search(r'\(char (\d+)\)', str(e))
            if m:
                pos = int(m.group(1))
                print(f"  Character at {pos}: {repr(val[pos])} (code: {ord(val[pos])})")
                print(f"  Surrounding text: {repr(val[max(0, pos-30):min(len(val), pos+30)])}")

# Also check workflow_history
row_hist = cur.execute("""
SELECT nodes, connections, nodeGroups FROM workflow_history WHERE workflowId = 'IGComBotWf9921XYZ'
""").fetchone()

for name, val in zip(['history.nodes', 'history.connections', 'history.nodeGroups'], row_hist):
    if val is not None:
        try:
            json.loads(val, strict=True)
            print(f"workflow_history.{name}: VALID (length {len(val)})")
        except Exception as e:
            print(f"workflow_history.{name}: ERROR -> {e}")

# Also check webhook_entity
print("\n--- webhook_entity ---")
for r in cur.execute("SELECT * FROM webhook_entity WHERE workflowId = 'IGComBotWf9921XYZ'").fetchall():
    print(r)
