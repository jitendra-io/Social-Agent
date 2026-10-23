import urllib.request
import json

payload = {
  "entry": [
    {
      "id": "17841425833721941",
      "time": 1729678800,
      "changes": [
        {
          "field": "comments",
          "value": {
            "id": "17999999999999999",
            "text": "This AI agent workflow is insanely good! How do you build this?",
            "from": {
              "id": "999888777",
              "username": "alex_tech_creator"
            },
            "media": {
              "id": "18012345678901234"
            }
          }
        }
      ]
    }
  ]
}

url = "https://compliant-phase-sierra-contemporary.trycloudflare.com/webhook/instagram-webhook"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    resp = urllib.request.urlopen(req)
    print("STATUS:", resp.status)
    print("RESPONSE:", resp.read().decode())
except Exception as e:
    print("ERROR:", e)
