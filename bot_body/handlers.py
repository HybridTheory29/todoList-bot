import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from django.conf import settings
import requests

user_router = Router()

def get_user_tasks(telegram_id):
    with sqlite3.connect('bot_db') as con:
        cursor = con.cursor()
        cursor.execute("""
        SELECT title, deadline 
        FROM bot_tasks 
        WHERE user_telegram_id = ?
        """, [str(telegram_id)])
        return cursor.fetchall()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    token = message.get_args()
    await message.answer('Привет! Этот бот будет присылать тебе уведомления о просроченных заданиях на сайте ToDo-List')
    if token:
        response = requests.post(
            f'{settings.DJANGO_SITE_URL}/api/confirm-telegram/',
            json={'token': token, 'chat_id': message.chat.id}
        )
        if response.status_code == 200:
            await message.answer("✅ Ваш аккаунт успешно привязан!")
        else:
            await message.answer("❌ Неверный токен привязки")

@user_router.message(Command('check_tasks'))
async def check_tasks(message: Message):
    tasks = get_user_tasks(message.from_user.id)

    if not tasks:
        await message.answer('У вас нет просроченных задач')
        return
    
    response = ['Просроченные задачи:']
    for title, deadline in tasks:
        response.append(f'{title} - до {deadline[:10]}')

    await message.answer('\n'.join(response))