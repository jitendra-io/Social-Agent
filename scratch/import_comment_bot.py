import sqlite3, json, uuid, datetime

with open('workflows/instagram_comment_bot.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

# Check if already exists
row = cur.execute("SELECT id, activeVersionId FROM workflow_entity WHERE name = 'Instagram Reel Comment Auto-Responder'").fetchone()

wf_id = row[0] if row else 'IGComBotWf9921XYZ'
version_id = row[1] if row else str(uuid.uuid4())
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Attach MySQL and Telegram credentials
mysql_cred = {"mySql": {"id": "EqWe2mFyNhEwmbEV", "name": "MySQL account"}}
tg_cred = {"telegramApi": {"id": "Gb75YCFSgLNADuv2", "name": "Telegram account"}}

for n in wf['nodes']:
    ntype = n.get('type', '')
    if 'mySql' in ntype:
        n['credentials'] = mysql_cred
    elif 'telegram' in ntype:
        n['credentials'] = tg_cred

nodes_str = json.dumps(wf['nodes'])
conns_str = json.dumps(wf['connections'])
settings_str = json.dumps({"executionOrder": "v1", "saveDataSuccessExecution": "all", "saveDataErrorExecution": "all"})

if row:
    cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, settings = ?, active = 1, updatedAt = ? WHERE id = ?", (nodes_str, conns_str, settings_str, now, wf_id))
    cur.execute("UPDATE workflow_history SET nodes = ?, connections = ?, updatedAt = ? WHERE versionId = ?", (nodes_str, conns_str, now, version_id))
else:
    cur.execute("""
    INSERT INTO workflow_entity (id, name, active, activeVersionId, nodes, connections, settings, staticData, pinData, versionId, triggerCount, createdAt, updatedAt)
    VALUES (?, 'Instagram Reel Comment Auto-Responder', 1, ?, ?, ?, ?, NULL, NULL, ?, 2, ?, ?)
    """, (wf_id, version_id, nodes_str, conns_str, settings_str, version_id, now, now))
    
    cur.execute("""
    INSERT INTO workflow_history (versionId, workflowId, nodes, connections, name, autosaved, createdAt, updatedAt, authors)
    VALUES (?, ?, ?, ?, 'Instagram Reel Comment Auto-Responder', 0, ?, ?, 'Jitendra Mishra')
    """, (version_id, wf_id, nodes_str, conns_str, now, now))

# Register webhooks in webhook_entity
cur.execute("DELETE FROM webhook_entity WHERE workflowId = ?", (wf_id,))
cur.execute("INSERT INTO webhook_entity (workflowId, webhookPath, method, node, webhookId, pathLength) VALUES (?, 'instagram-webhook', 'GET', 'Meta Webhook Verification (GET)', 'instagram-verification', 1)", (wf_id,))
cur.execute("INSERT INTO webhook_entity (workflowId, webhookPath, method, node, webhookId, pathLength) VALUES (?, 'instagram-webhook', 'POST', 'Meta Inbound Comments (POST)', 'instagram-comments', 1)", (wf_id,))

con.commit()
con.close()
print(f"Successfully imported and activated Instagram Reel Comment Bot (ID: {wf_id})!")
