import os

MAX_TOKEN = os.getenv("MAX_BOT_TOKEN")

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    "hi_right_now_secret"
)

API_URL = "https://platform-api2.max.ru"

WEBHOOK_URL = (
    "https://web-production-223a3d.up.railway.app/webhook"
)
