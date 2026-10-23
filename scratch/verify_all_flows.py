import urllib.request
import json
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

results = {}

# 1. Check Media Engine
try:
    resp = urllib.request.urlopen("http://localhost:8000/health", timeout=5)
    results["media_engine"] = ("PASS", resp.read().decode().strip())
except Exception as e:
    results["media_engine"] = ("FAIL", str(e))

# 2. Check Dev Bridge
try:
    resp = urllib.request.urlopen("http://localhost:8050/health", timeout=5)
    results["dev_bridge"] = ("PASS", resp.read().decode().strip())
except Exception as e:
    results["dev_bridge"] = ("FAIL", str(e))

# 3. Check n8n workflows in SQLite
try:
    con = sqlite3.connect("n8n_data/database.sqlite")
    cur = con.cursor()
    wfs = cur.execute("SELECT id, name, active FROM workflow_entity").fetchall()
    active_count = sum(1 for w in wfs if w[2] == 1)
    results["n8n_workflows"] = ("PASS", f"{active_count}/{len(wfs)} active", [(w[1], "ACTIVE" if w[2] == 1 else "INACTIVE") for w in wfs])
    con.close()
except Exception as e:
    results["n8n_workflows"] = ("FAIL", str(e))

# 4. Check Telegram Webhook
try:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    resp = urllib.request.urlopen(url, timeout=5)
    info = json.loads(resp.read().decode())
    tg_url = info.get("result", {}).get("url", "")
    pending = info.get("result", {}).get("pending_update_count", 0)
    last_err = info.get("result", {}).get("last_error_message", "None")
    results["telegram_webhook"] = ("PASS", f"URL: {tg_url} | Pending: {pending} | LastErr: {last_err}")
except Exception as e:
    results["telegram_webhook"] = ("FAIL", str(e))

# 5. Check Cloudflare Tunnel Public Webhook for Instagram Comment Bot
tunnel_url = "https://lightweight-navy-bookmark-intelligence.trycloudflare.com"
try:
    url = f"{tunnel_url}/webhook/instagram-webhook?hub.mode=subscribe&hub.verify_token=agency_nova_secure_token_2026&hub.challenge=test_meta_ok_999"
    resp = urllib.request.urlopen(url, timeout=10)
    body = resp.read().decode().strip()
    if resp.status == 200 and body == "test_meta_ok_999":
        results["instagram_webhook_challenge"] = ("PASS", "200 OK challenge match")
    else:
        results["instagram_webhook_challenge"] = ("WARN", f"Status: {resp.status}, Body: {body}")
except Exception as e:
    results["instagram_webhook_challenge"] = ("FAIL", str(e))

# 6. Check WhatsApp Webhook Verification
try:
    wa_token = os.environ.get("WHATSAPP_VERIFY_TOKEN", "agency_nova_secure_token_2026")
    url = f"{tunnel_url}/webhook/whatsapp-webhook?hub.mode=subscribe&hub.verify_token={wa_token}&hub.challenge=test_wa_challenge"
    resp = urllib.request.urlopen(url, timeout=10)
    body = resp.read().decode().strip()
    results["whatsapp_webhook_challenge"] = ("PASS" if resp.status == 200 else "WARN", f"Status: {resp.status}, Body: {body}")
except Exception as e:
    results["whatsapp_webhook_challenge"] = ("FAIL", str(e))

print("=== SYSTEM HEALTH VERIFICATION RESULTS ===")
for k, v in results.items():
    print(f"[{v[0]}] {k}: {v[1]}")
    if len(v) > 2:
        for item in v[2]:
            print(f"    - {item[0]}: {item[1]}")
