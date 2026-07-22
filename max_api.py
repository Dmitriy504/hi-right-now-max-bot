import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://platform-api2.max.ru"

TOKEN = os.getenv("MAX_BOT_TOKEN")

if not TOKEN:
    raise Exception("MAX_BOT_TOKEN is empty!")

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}


def send_text(chat_id: int, text: str):
    """
    Отправка текстового сообщения в чат MAX
    """

    body = {
        "text": text
    }

    try:
        response = requests.post(
            f"{API_URL}/messages",
            params={
                "chat_id": chat_id
            },
            headers=HEADERS,
            json=body,
            verify=False,
            timeout=30
        )

        print("=" * 50)
        print("SEND MESSAGE")
        print("Status:", response.status_code)
        print("Response:", response.text)
        print("=" * 50)

        return response

    except Exception as e:
        print("=" * 50)
        print("SEND ERROR")
        print(e)
        print("=" * 50)
        return None
