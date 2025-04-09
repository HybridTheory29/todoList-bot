import sqlite3
from django.db import connection

def sync_to_bot():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT id, title, deadline 
        FROM tasks_task 
        WHERE telegram_synced = 0
        """)
        tasks = cursor.fetchall()

    with sqlite3.connect('bot_db') as bot_con:
        bot_cursor = bot_con.cursor()
        
        for task_id, title, deadline in tasks:
            try:
                bot_cursor.execute("""
                INSERT INTO bot_tasks 
                (django_task_id, title, deadline, user_telegram_id)
                VALUES (?, ?, ?, ?)
                """, (task_id, title, deadline.isoformat(), None))
                
                cursor.execute("""
                UPDATE tasks_task 
                SET telegram_synced = 1 
                WHERE id = ?
                """, [task_id])
                
            except sqlite3.IntegrityError:
                print(f"Задача {task_id} уже существует в БД бота")