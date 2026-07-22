import os
import requests

API_URL = "https://platform-api2.max.ru"

TOKEN = os.getenv("MAX_BOT_TOKEN")

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}


def send_text(chat_id: int, text: str):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(
        f"{API_URL}/messages",
        headers=HEADERS,
        json=payload,
        verify=False,
        timeout=30
    )

    print("SEND:", r.status_code, r.text)
