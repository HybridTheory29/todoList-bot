from sqlite3 import connect

def init_db():
    with connect('bot_db') as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bot_tasks (
                id INTEGER PRIMARY KEY,
                django_task_id INTEGER UNIQUE,  # Связь с основной БД
                title TEXT,
                deadline TEXT,
                user_telegram_id TEXT
                       )               
                       """)
        con.commit()