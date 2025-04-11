import sqlite3, aiohttp, asyncio, logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from django.conf import settings
import requests

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Этот бот будет присылать тебе уведомления о просроченных заданиях на сайте ToDo-List')
    

async def check_tasks():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://yourdjango.com/api/get_overdue_tasks/') as resp:
                    data = await resp.json()
                    for telegram_id, user_data in data.items():
                        for task in user_data['tasks']:
                            message = (
                                f"🚨 Просроченная задача!\n"
                                f"Название: {task['title']}\n"
                                f"Дедлайн: {task['due_date']}"
                            )
                            await bot.send_message(
                                chat_id=user_data['chat_id'],
                                text=message
                            )
        except Exception as e:
            logging.error(f"Ошибка при проверке задач: {e}")
        
        await asyncio.sleep(3600)  # Проверка каждый час