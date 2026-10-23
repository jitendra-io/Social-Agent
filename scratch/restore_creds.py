import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

mysql_cred = {"mySql": {"id": "EqWe2mFyNhEwmbEV", "name": "MySQL account"}}
tg_cred = {"telegramApi": {"id": "Gb75YCFSgLNADuv2", "name": "Telegram account"}}

for table in ['workflow_entity', 'workflow_history']:
    col = 'id' if table == 'workflow_entity' else 'versionId'
    target_val = 'Y6ResnEyOHxuJIdI' if table == 'workflow_entity' else 'bfcd1622-ddb3-4b41-a1d2-200c59f279ef'
    
    row = cur.execute(f"SELECT nodes FROM {table} WHERE {col} = ?", (target_val,)).fetchone()
    nodes = json.loads(row[0])
    
    for n in nodes:
        ntype = n.get('type', '')
        if 'mySql' in ntype:
            n['credentials'] = mysql_cred
        elif 'telegram' in ntype:
            n['credentials'] = tg_cred
            
    cur.execute(f"UPDATE {table} SET nodes = ? WHERE {col} = ?", (json.dumps(nodes), target_val))
    print(f"Restored credentials in {table}!")

con.commit()
con.close()
print("All credentials restored in SQLite!")
