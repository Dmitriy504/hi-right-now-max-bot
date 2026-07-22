from database import user_exists, add_user
from fastapi import FastAPI
import urllib3
import json

from max_api import send_text

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(title="Hi Right Now MAX Bot")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(data: dict):

    print("=" * 60)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("=" * 60)

    if data.get("update_type") != "message_created":
        return {"success": True}

    message = data.get("message", {})

    recipient = message.get("recipient", {})
    chat_id = recipient.get("chat_id")

    sender = message.get("sender", {})
    user_id = sender.get("user_id")
    first_name = sender.get("first_name", "")
    last_name = sender.get("last_name", "")

    body = message.get("body", {})
    text = body.get("text", "").strip()

    # Если пользователь написал "Привет"
    if text.lower() == "привет":

        # Приветствие пользователю
        send_text(
            chat_id,
            "👋 Привет!\n\n"
            "Добро пожаловать в Hi Right Now!\n\n"
            "📸 Отправь фотографию и подпись:\n\n"
            "«Привет, я сейчас...»\n\n"
            "Я превращу это в красивый пост."
        )

        # Уведомление администратора (пока в этот же чат)
        send_text(
            chat_id,
            f"🔔 Администратор\n\n"
            f"Пользователь запустил бота.\n\n"
            f"👤 ID: {user_id}\n"
            f"Имя: {first_name} {last_name}"
        )

    # Пока просто подтверждаем получение фотографии
    attachments = body.get("attachments", [])

    if attachments:
        print("ATTACHMENTS:")
        print(json.dumps(attachments, indent=2, ensure_ascii=False))

        send_text(
            chat_id,
            "📸 Фото получено!\n\n"
            "Скоро я научусь создавать красивые посты по фотографии."
        )

    return {"success": True}
