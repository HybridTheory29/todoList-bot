import sqlite3

def init_db():
    conn = sqlite3.connect('todoList-bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            site_user_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_user(telegram_id: int, site_user_id: int):
    conn = sqlite3.connect('todoList-bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (telegram_id, site_user_id)
        VALUES (?, ?)
    ''', (telegram_id, site_user_id))
    conn.commit()
    conn.close()

def get_site_user_id(telegram_id: int) -> int | None:
    conn = sqlite3.connect('todoList-bot.db')
    cursor = conn.cursor
    cursor.execute('SELECT site_user_id FROM users WHERE telegram_id = ?', (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None