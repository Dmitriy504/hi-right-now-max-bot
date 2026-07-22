from fastapi import FastAPI
import urllib3

from max_api import send_text

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(title="Hi Right Now MAX Bot")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(data: dict):

    import json

print("=" * 60)
print(json.dumps(data, indent=2, ensure_ascii=False))
print("=" * 60)

    if data.get("update_type") == "message_created":

        message = data.get("message", {})

        chat_id = message["recipient"]["chat_id"]

        text = message.get("body", {}).get("text", "")

        if text.lower() == "привет":

            send_text(
                chat_id,
                "👋 Привет!\n\n"
                "Отправь фотографию 📸\n"
                "и подпись:\n\n"
                "«Привет, я сейчас...»"
            )

    return {"success": True}
