from fastapi import FastAPI
import urllib3
import json

from max_api import send_text
from database import user_exists, add_user

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

    # Новый пользователь
    if not user_exists(user_id):

        add_user(
            user_id,
            first_name,
            last_name
        )

        send_text(
            chat_id,
            "👋 Привет!\n\n"
            "Добро пожаловать в Hi Right Now!\n\n"
            "📸 Отправь фотографию и подпись:\n\n"
            "«Привет, я сейчас...»\n\n"
            "Я превращу это в красивый пост."
        )

        # Пока уведомление отправляется в этот же чат.
        # Позже заменим chat_id на ID администратора.
        send_text(
            chat_id,
            f"🔔 Новый пользователь!\n\n"
            f"👤 ID: {user_id}\n"
            f"Имя: {first_name} {last_name}"
        )

        return {"success": True}

    # Повторный пользователь
    if text.lower() == "привет":

        send_text(
            chat_id,
            "👋 С возвращением!\n\n"
            "Отправь фотографию и подпись.\n"
            "Я помогу сделать красивый пост."
        )

    # Проверка вложений
    attachments = body.get("attachments", [])

    if attachments:

        print("ATTACHMENTS:")
        print(json.dumps(attachments, indent=2, ensure_ascii=False))

        send_text(
            chat_id,
            "📸 Фото получено!\n\n"
            "Скоро я научусь анализировать изображения и создавать посты."
        )

    return {"success": True}
