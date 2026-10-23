import sqlite3, json, datetime

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%f')[:-3]

# Update social_pipeline (ID: fk5xv1XIQgn8rgwB)
with open('workflows/social_pipeline.json', 'r', encoding='utf-8') as f:
    sp_wf = json.load(f)

mysql_cred = {"mySql": {"id": "EqWe2mFyNhEwmbEV", "name": "MySQL account"}}
tg_cred = {"telegramApi": {"id": "Gb75YCFSgLNADuv2", "name": "Telegram account"}}

for n in sp_wf['nodes']:
    ntype = n.get('type', '')
    if 'mySql' in ntype:
        n['credentials'] = mysql_cred
    elif 'telegram' in ntype:
        n['credentials'] = tg_cred

sp_nodes = json.dumps(sp_wf['nodes'])
sp_conns = json.dumps(sp_wf['connections'])

cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, updatedAt = ? WHERE id = 'fk5xv1XIQgn8rgwB'", (sp_nodes, sp_conns, now))
cur.execute("UPDATE workflow_history SET nodes = ?, connections = ?, updatedAt = ? WHERE workflowId = 'fk5xv1XIQgn8rgwB'", (sp_nodes, sp_conns, now))
print("Synced Social Pipeline.")

con.commit()
con.close()
