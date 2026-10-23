import sqlite3, json

with open('workflows/social_publisher.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

nodes_str = json.dumps(wf['nodes'])
conns_str = json.dumps(wf['connections'])

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

# Get activeVersionId for QBOru6Ia63x8N62K
row = cur.execute("SELECT activeVersionId FROM workflow_entity WHERE id = 'QBOru6Ia63x8N62K'").fetchone()
active_ver = row[0] if row else None

cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ? WHERE id = 'QBOru6Ia63x8N62K'", (nodes_str, conns_str))
if active_ver:
    cur.execute("UPDATE workflow_history SET nodes = ?, connections = ? WHERE versionId = ?", (nodes_str, conns_str, active_ver))

# Restore YouTube credentials
yt_cred = {"youTubeOAuth2Api": {"id": "TEOol5JeDfBm4yVU", "name": "YouTube account"}}
mysql_cred = {"mySql": {"id": "EqWe2mFyNhEwmbEV", "name": "MySQL account"}}
tg_cred = {"telegramApi": {"id": "Gb75YCFSgLNADuv2", "name": "Telegram account"}}

for table in ['workflow_entity', 'workflow_history']:
    col = 'id' if table == 'workflow_entity' else 'versionId'
    target_val = 'QBOru6Ia63x8N62K' if table == 'workflow_entity' else active_ver
    if not target_val: continue
    
    r = cur.execute(f"SELECT nodes FROM {table} WHERE {col} = ?", (target_val,)).fetchone()
    if not r: continue
    nodes = json.loads(r[0])
    
    for n in nodes:
        ntype = n.get('type', '')
        if 'youTube' in ntype:
            n['credentials'] = yt_cred
        elif 'mySql' in ntype:
            n['credentials'] = mysql_cred
        elif 'telegram' in ntype:
            n['credentials'] = tg_cred
            
    cur.execute(f"UPDATE {table} SET nodes = ? WHERE {col} = ?", (json.dumps(nodes), target_val))

con.commit()
con.close()
print("Synced social_publisher to SQLite and restored all credentials!")
