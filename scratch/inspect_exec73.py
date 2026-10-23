import sqlite3
import json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

row = cur.execute("SELECT data FROM execution_data WHERE executionId = 73").fetchone()
if row:
    raw = row[0]
    try:
        parsed = json.loads(raw)
        print("Keys:", parsed[0] if isinstance(parsed, list) else parsed.keys())
        # Check nodeExecutionStack or resultData
        print("Content dump:")
        print(raw[:2000])
    except Exception as e:
        print("Error parsing:", e)
        print(raw[:1000])
