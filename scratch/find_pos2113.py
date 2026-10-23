import sqlite3
import subprocess

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

found = 0
for table in tables:
    cur.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cur.fetchall()]
    try:
        rows = cur.execute(f"SELECT * FROM {table}").fetchall()
    except Exception:
        continue
    for row in rows:
        for col_name, val in zip(cols, row):
            if isinstance(val, str) and len(val) >= 2113:
                # Test exact JSON.parse with Node
                p = subprocess.run(
                    ['node', '-e', 'try { JSON.parse(process.argv[1]); } catch(e) { console.log(e.message); process.exit(1); }', val],
                    capture_output=True,
                    text=True
                )
                if p.returncode != 0:
                    found += 1
                    print(f"MATCH in {table}.{col_name} (row id: {row[0] if len(row) > 0 else '?'}) -> {p.stdout.strip()}")
                    if "position 2113" in p.stdout:
                        print(f"*** EXACT TARGET FOUND in {table}.{col_name} ***")
                        print("Chars around 2113:")
                        print(repr(val[2090:2140]))

print(f"Scan complete. Total errors found: {found}")
