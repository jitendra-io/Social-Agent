import sqlite3
import subprocess

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

nodes_str = cur.execute("SELECT nodes FROM workflow_history WHERE workflowId = 'IGComBotWf9921XYZ'").fetchone()[0]

p = subprocess.run(
    ['node', '-e', 'try { JSON.parse(process.argv[1]); console.log("HISTORY NODE PARSE SUCCESS"); } catch(e) { console.error("HISTORY NODE PARSE FAIL:", e.message); }', nodes_str],
    capture_output=True,
    text=True
)
print("Result with node:", p.stdout, p.stderr)
