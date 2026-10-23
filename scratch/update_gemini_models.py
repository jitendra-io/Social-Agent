import sqlite3

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()

# Replace gemini-1.5-flash with gemini-3.8-flash in all workflow nodes
rows = cur.execute("SELECT id, name, nodes FROM workflow_entity").fetchall()
updated_count = 0

for wf_id, name, nodes_str in rows:
    if 'gemini-1.5-flash' in nodes_str:
        new_nodes_str = nodes_str.replace('gemini-1.5-flash', 'gemini-3.8-flash')
        cur.execute("UPDATE workflow_entity SET nodes = ? WHERE id = ?", (new_nodes_str, wf_id))
        print(f"Updated {name} ({wf_id}) to gemini-3.8-flash")
        updated_count += 1

con.commit()
con.close()
print(f"Successfully updated {updated_count} workflows to gemini-3.8-flash!")
