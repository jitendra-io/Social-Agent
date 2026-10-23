import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_ADMIN_ID")
url = f"https://api.telegram.org/bot{token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": (
        "🎬 *EXECUTIVE REVIEW: POST #2*\n\n"
        "📌 *Topic:* Autonomous AI Agency Revolution\n"
        "🪝 *Hook:* \"Why manual business operations are dead in 2026\"\n\n"
        "📝 *Caption:*\n"
        "The autonomous business revolution is here. Are you adapting? 🚀 #ai #automation #tech #future #business\n\n"
        "👇 *Select an executive action below to publish:*"
    ),
    "parse_mode": "Markdown",
    "reply_markup": json.dumps({
        "inline_keyboard": [
            [
                {"text": "✅ Approve & Post", "callback_data": "approve_2"},
                {"text": "✏️ Edit Caption", "callback_data": "edit_2"}
            ],
            [
                {"text": "🔄 Regenerate", "callback_data": "regen_2"},
                {"text": "💡 Suggest Next Step", "callback_data": "suggest_2"}
            ]
        ]
    })
}

resp = requests.post(url, data=payload)
print("STATUS:", resp.status_code)
print("OK:", resp.json().get("ok"))
