import sqlite3
import json

def parse_flatted(data):
    # standard flatted parse in python
    if isinstance(data, str):
        data = json.loads(data)
    
    root = data[0]
    
    def resolve(val):
        if isinstance(val, str) and val.isdigit():
            idx = int(val)
            if idx < len(data):
                return resolve(data[idx])
        elif isinstance(val, list):
            return [resolve(x) for x in val]
        elif isinstance(val, dict):
            return {k: resolve(v) for k, v in val.items()}
        return val
        
    return resolve(root)

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT data FROM execution_data WHERE executionId = 73").fetchone()
if row:
    parsed = parse_flatted(row[0])
    run_data = parsed.get('resultData', {}).get('runData', {})
    print("Nodes executed in runData:", list(run_data.keys()))
    for node_name, node_runs in run_data.items():
        print(f"\n--- Node: {node_name} ---")
        for run in node_runs:
            print("Execution time:", run.get('executionTime'))
            if 'error' in run:
                print("ERROR:", run['error'])
            if 'data' in run:
                out = run['data'].get('main', [[]])[0]
                print(f"Output count: {len(out)}")
                if out:
                    print("Sample output:", str(out[0])[:300])
