import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is empty!")

print("DATABASE_URL =", DATABASE_URL)

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
)
""")


def user_exists(user_id):
    cur.execute(
        "SELECT 1 FROM users WHERE user_id=%s",
        (user_id,)
    )
    return cur.fetchone() is not None


def add_user(user_id, first_name="", last_name=""):
    cur.execute(
        """
        INSERT INTO users(user_id, first_name, last_name)
        VALUES (%s,%s,%s)
        ON CONFLICT (user_id) DO NOTHING
        """,
        (
            user_id,
            first_name,
            last_name
        )
    )
