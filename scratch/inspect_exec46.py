import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT data FROM execution_data WHERE executionId=46").fetchone()
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
print("Keys in resolved:", resolved.keys())
result_data = resolved.get('resultData', {})
run_data = result_data.get('runData', {})
print("Executed nodes in runData:", list(run_data.keys()))
for node_name, runs in run_data.items():
    print(f"\n--- Node: {node_name} ---")
    for r in runs:
        print(f"Status: {r.get('executionStatus')}, Error: {r.get('error')}")
        if r.get('error'):
            print("ERROR DETAILS:", r.get('error'))
