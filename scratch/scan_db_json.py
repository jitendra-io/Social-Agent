import sqlite3
import subprocess

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

for table in tables:
    cur.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cur.fetchall()]
    rows = cur.execute(f"SELECT * FROM {table}").fetchall()
    for row in rows:
        for col_name, val in zip(cols, row):
            if isinstance(val, str) and (val.startswith('{') or val.startswith('[')):
                # Test with node JSON.parse
                p = subprocess.run(
                    ['node', '-e', 'try { JSON.parse(process.argv[1]); } catch(e) { console.log(e.message); process.exit(1); }', val],
                    capture_output=True,
                    text=True
                )
                if p.returncode != 0:
                    print(f"FAILED: table {table}, col {col_name}, row {row[:2]}: {p.stdout.strip()}")
print("Scan complete.")
