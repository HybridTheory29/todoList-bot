import sqlite3, aiohttp, asyncio, logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from standart_run import bot
from decouple import config
import requests

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Этот бот будет присылать тебе уведомления о просроченных заданиях на сайте ToDo-List\n\nЧтобы проверить состояние задач, введите команду - </check>')

def get_overdue_tasks():
    try:
        response = requests.get(config('API_URL'))
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

@user_router.message(Command("check"))
async def cmd_ckeck_tasks(message: Message):
    chat_id = message.chat.id
    tasks = get_overdue_tasks()
    if tasks:
        message = "🔔 Просроченные задачи:\n\n"
        for task in tasks:
            message += f"• {task['title']} (до {task['deadline']})\n"
    else:
        message = "✅ Нет просроченных задач"

    await bot.send_message(chat_id=chat_id, text=message)