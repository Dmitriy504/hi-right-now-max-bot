from fastapi import FastAPI
import os
import requests

app = FastAPI(title="Hi Right Now MAX Bot")

API_URL = "https://platform-api2.max.ru"

TOKEN = os.getenv("MAX_BOT_TOKEN")
SECRET = os.getenv("WEBHOOK_SECRET", "hi_right_now_secret")

WEBHOOK_URL = "https://web-production-223a3d.up.railway.app/webhook"


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/register-webhook")
async def register_webhook():

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "url": WEBHOOK_URL,
        "update_types": [
            "message_created",
            "bot_started"
        ],
        "secret": SECRET
    }

    r = requests.post(
        f"{API_URL}/subscriptions",
        headers=headers,
        json=payload,
        timeout=30
    )

    return {
        "status": r.status_code,
        "response": r.text
    }


@app.post("/webhook")
async def webhook(data: dict):

    print("=" * 60)
    print(data)
    print("=" * 60)

    return {"success": True}
