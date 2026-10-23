import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables in sqlite:", tables)

for t in tables:
    if any(k in t.lower() for k in ['publish', 'version', 'workflow', 'history', 'outbox']):
        print(f"\n--- Table: {t} ---")
        cur.execute(f"PRAGMA table_info({t})")
        print("Columns:", [c[1] for c in cur.fetchall()])
        rows = cur.execute(f"SELECT * FROM {t}").fetchall()
        print(f"Row count: {len(rows)}")
        for r in rows[:10]:
            print(" ", r if len(str(r)) < 200 else str(r)[:200] + "...")
