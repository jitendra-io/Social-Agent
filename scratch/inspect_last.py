import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT data FROM execution_data ORDER BY executionId DESC LIMIT 1").fetchone()
raw = json.loads(row[0])

# flattener for n8n execution data serialization
def resolve(item):
    if isinstance(item, str) and item.isdigit() and int(item) < len(raw):
        return resolve(raw[int(item)])
    if isinstance(item, list):
        return [resolve(x) for x in item]
    if isinstance(item, dict):
        return {k: resolve(v) for k, v in item.items()}
    return item

resolved = resolve(raw[0])
res = resolved['resultData']
print("resultData keys:", res.keys())
print("runData keys:", list(res.get('runData', {}).keys()))
print("lastNodeExecuted:", res.get('lastNodeExecuted'))
