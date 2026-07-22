import requests

from config import (
    API_URL,
    MAX_TOKEN,
    WEBHOOK_SECRET,
    WEBHOOK_URL,
)

headers = {
    "Authorization": MAX_TOKEN,
    "Content-Type": "application/json",
}

payload = {
    "url": WEBHOOK_URL,
    "update_types": [
        "message_created",
        "bot_started"
    ],
    "secret": WEBHOOK_SECRET,
}

response = requests.post(
    f"{API_URL}/subscriptions",
    headers=headers,
    json=payload,
)

print(response.status_code)
print(response.text)
