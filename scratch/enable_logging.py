import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

row = cur.execute("SELECT settings FROM workflow_entity WHERE id = 'Y6ResnEyOHxuJIdI'").fetchone()
settings = json.loads(row[0]) if row and row[0] else {}
settings['saveDataSuccessExecution'] = 'all'
settings['saveDataErrorExecution'] = 'all'
settings['saveExecutionProgress'] = True
settings['saveManualExecutions'] = True
cur.execute("UPDATE workflow_entity SET settings = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (json.dumps(settings),))

con.commit()
con.close()
print("Execution logging enabled successfully!")
