import urllib.request
import json
import time

url = "http://localhost:5678/webhook/tg-webhook-dispatcher/webhook"
secret = "Y6ResnEyOHxuJIdI_tg-trigger-1"
payload = {
    "update_id": int(time.time()),
    "message": {
        "message_id": 201,
        "from": {"id": 8226006494, "first_name": "Jitendra", "is_bot": False},
        "chat": {"id": 8226006494, "first_name": "Jitendra", "type": "private"},
        "date": int(time.time()),
        "text": "/post 3 insane AI tools that will replace agencies in 2026"
    }
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-telegram-bot-api-secret-token": secret
    }
)

print("Triggering /post pipeline...")
try:
    resp = urllib.request.urlopen(req, timeout=15)
    print("STATUS:", resp.status)
    print("RESPONSE:", resp.read().decode())
except Exception as e:
    print("ERROR:", e)
