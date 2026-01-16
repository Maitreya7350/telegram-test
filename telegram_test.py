import requests
import os

TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "✅ Telegram test successful.\nGitHub Actions can send messages.",
}

requests.post(url, data=data, timeout=20)
