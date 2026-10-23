import sqlite3, json, datetime

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%f')[:-3]

# 1. Update telegram_dispatcher (ID: Y6ResnEyOHxuJIdI)
with open('workflows/telegram_dispatcher.json', 'r', encoding='utf-8') as f:
    td_wf = json.load(f)

# Restore MySQL and Telegram credentials
mysql_cred = {"mySql": {"id": "EqWe2mFyNhEwmbEV", "name": "MySQL account"}}
tg_cred = {"telegramApi": {"id": "Gb75YCFSgLNADuv2", "name": "Telegram account"}}

for n in td_wf['nodes']:
    ntype = n.get('type', '')
    if 'mySql' in ntype:
        n['credentials'] = mysql_cred
    elif 'telegram' in ntype:
        n['credentials'] = tg_cred

td_nodes = json.dumps(td_wf['nodes'])
td_conns = json.dumps(td_wf['connections'])

cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, updatedAt = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (td_nodes, td_conns, now))
cur.execute("UPDATE workflow_history SET nodes = ?, connections = ?, updatedAt = ? WHERE workflowId = 'Y6ResnEyOHxuJIdI'", (td_nodes, td_conns, now))
print("Synced Telegram Dispatcher.")

# 2. Update callback_handler (ID: lHzSdAxS3MBlM7nL)
with open('workflows/callback_handler.json', 'r', encoding='utf-8') as f:
    cb_wf = json.load(f)

for n in cb_wf['nodes']:
    ntype = n.get('type', '')
    if 'mySql' in ntype:
        n['credentials'] = mysql_cred
    elif 'telegram' in ntype:
        n['credentials'] = tg_cred

cb_nodes = json.dumps(cb_wf['nodes'])
cb_conns = json.dumps(cb_wf['connections'])

cur.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, updatedAt = ? WHERE id = 'lHzSdAxS3MBlM7nL'", (cb_nodes, cb_conns, now))
cur.execute("UPDATE workflow_history SET nodes = ?, connections = ?, updatedAt = ? WHERE workflowId = 'lHzSdAxS3MBlM7nL'", (cb_nodes, cb_conns, now))
print("Synced Callback Handler.")

con.commit()
con.close()
