import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher
from decouple import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher()

def get_overdue_tasks():
    try:
        response = requests.get(config('API_URL'))
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

async def send_overdue_notification():
    tasks = get_overdue_tasks()
    if tasks:
        message = "🔔 Просроченные задачи:\n\n"
        for task in tasks:
            message += f"• {task['title']} (до {task['deadline']})\n"
    else:
        message = "✅ Нет просроченных задач"

    await bot.send_message(chat_id=config('CHAT_ID'), text=message)

async def main():
    await send_overdue_notification()
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())