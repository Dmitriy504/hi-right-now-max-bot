import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
)
""")

conn.commit()


def user_exists(user_id: int) -> bool:
    cursor.execute(
        "SELECT 1 FROM users WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchone() is not None


def add_user(user_id: int, first_name: str, last_name: str):
    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, first_name, last_name)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            first_name,
            last_name
        )
    )

    conn.commit()
