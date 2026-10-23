import sqlite3, json

con = sqlite3.connect('n8n_data/database.sqlite')
cur = con.cursor()
row = cur.execute("SELECT nodes FROM workflow_entity WHERE id='Y6ResnEyOHxuJIdI'").fetchone()
nodes = json.loads(row[0])

def make_rule(cmd):
    return {
        "conditions": {
            "options": {
                "caseSensitive": False,
                "leftValue": "",
                "typeValidation": "loose",
                "version": 1
            },
            "conditions": [
                {
                    "leftValue": "={{ $('Telegram Trigger').item.json.message.text.split(' ')[0] }}",
                    "rightValue": cmd,
                    "operator": {
                        "type": "string",
                        "operation": "equals"
                    }
                }
            ],
            "combinator": "and"
        }
    }

for n in nodes:
    if n.get('name') == 'Command Router':
        n['parameters'] = {
            "mode": "rules",
            "rules": {
                "values": [
                    make_rule("/status"),
                    make_rule("/post"),
                    make_rule("/buildsite"),
                    make_rule("/remember"),
                    make_rule("/recall")
                ]
            },
            "options": {
                "fallbackOutput": 5
            }
        }
        print("Updated Command Router with valid Switch v3 rules!")

cur.execute("UPDATE workflow_entity SET nodes = ? WHERE id = 'Y6ResnEyOHxuJIdI'", (json.dumps(nodes),))
con.commit()
con.close()
print("Saved to n8n database.sqlite!")
