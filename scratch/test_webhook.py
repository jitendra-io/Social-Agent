import urllib.request
import time

time.sleep(3)
url = "http://localhost:5678/webhook/instagram-webhook?hub.mode=subscribe&hub.verify_token=agency_nova_secure_token_2026&hub.challenge=test_local_check"
try:
    resp = urllib.request.urlopen(url)
    print("STATUS:", resp.status)
    print("BODY:", resp.read().decode())
except Exception as e:
    print("ERROR:", e)
