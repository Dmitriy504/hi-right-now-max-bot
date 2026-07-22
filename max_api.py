import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://platform-api2.max.ru"

TOKEN = os.getenv("MAX_BOT_TOKEN")

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}


def send_text(chat_id: int, text: str):

    body = {
        "text": text
    }

    r = requests.post(
        f"{API_URL}/messages",
        params={
            "chat_id": chat_id
        },
        headers=HEADERS,
        json=body,
        verify=False,
        timeout=30
    )

    print("SEND:", r.status_code)
    print(r.text)
