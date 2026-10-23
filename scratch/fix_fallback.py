import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

for table in ['workflow_entity', 'workflow_history']:
    col = 'id' if table == 'workflow_entity' else 'versionId'
    target_val = 'Y6ResnEyOHxuJIdI' if table == 'workflow_entity' else 'bfcd1622-ddb3-4b41-a1d2-200c59f279ef'
    
    row = cur.execute(f"SELECT nodes FROM {table} WHERE {col} = ?", (target_val,)).fetchone()
    if not row:
        continue
    nodes = json.loads(row[0])
    for n in nodes:
        if n.get('name') == 'Command Router':
            n['parameters']['options']['fallbackOutput'] = 'extra'
            print(f"Fixed fallbackOutput in {table}!")
    
    cur.execute(f"UPDATE {table} SET nodes = ? WHERE {col} = ?", (json.dumps(nodes), target_val))

con.commit()
con.close()
print("Saved fallbackOutput: 'extra' to both tables!")
