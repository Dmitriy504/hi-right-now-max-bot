from fastapi import FastAPI
import json
import urllib3
import database as db

from database import user_exists, add_user
from max_api import send_text

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(title="Hi Right Now MAX Bot")

# Создаем таблицу настроек
db.cur.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")


def set_admin_chat(chat_id: int):
    db.cur.execute(
        """
        INSERT INTO settings(key, value)
        VALUES ('admin_chat', %s)
        ON CONFLICT (key)
        DO UPDATE SET value = EXCLUDED.value
        """,
        (str(chat_id),),
    )


def get_admin_chat():
    db.cur.execute(
        "SELECT value FROM settings WHERE key='admin_chat'"
    )

    row = db.cur.fetchone()

    if row:
        return int(row[0])

    return None


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
    sender = message.get("sender", {})
    body = message.get("body", {})

    chat_id = recipient.get("chat_id")
    user_id = sender.get("user_id")

    first_name = sender.get("first_name", "")
    last_name = sender.get("last_name", "")

    text = body.get("text", "").strip()
    attachments = body.get("attachments", [])

    if not chat_id or not user_id:
        return {"success": True}
            # Команда назначения администратора
    if text.lower() == "/admin":
        set_admin_chat(chat_id)

        send_text(
            chat_id,
            "✅ Этот чат назначен администратором."
        )

        return {"success": True}

    admin_chat = get_admin_chat()

    is_new_user = not user_exists(user_id)

    # Новый пользователь
    if is_new_user:

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

        if admin_chat and admin_chat != chat_id:

            full_name = f"{first_name} {last_name}".strip()

            send_text(
                admin_chat,
                f"🆕 Новый пользователь!\n\n"
                f"👤 {full_name}\n"
                f"🆔 {user_id}\n"
                f"💬 Chat ID: {chat_id}"
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

    # Проверяем наличие вложений
    if attachments:

        print("ATTACHMENTS:")
        print(json.dumps(
            attachments,
            indent=2,
            ensure_ascii=False
        ))

        send_text(
            chat_id,
            "📸
                # Уведомление админу о полученном фото
        if admin_chat and admin_chat != chat_id:

            full_name = f"{first_name} {last_name}".strip()

            send_text(
                admin_chat,
                f"📷 Новое фото\n\n"
                f"👤 {full_name}\n"
                f"🆔 {user_id}\n"
                f"💬 Chat ID: {chat_id}\n"
                f"📎 Вложений: {len(attachments)}\n\n"
                f"{text if text else 'Без подписи'}"
            )

    # Обычное текстовое сообщение
    elif text:

        if admin_chat and admin_chat != chat_id:

            full_name = f"{first_name} {last_name}".strip()

            send_text(
                admin_chat,
                f"💬 Новое сообщение\n\n"
                f"👤 {full_name}\n"
                f"🆔 {user_id}\n"
                f"💬 Chat ID: {chat_id}\n\n"
                f"{text}"
            )

    return {"success": True}
