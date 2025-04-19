import sqlite3, aiohttp, asyncio, logging, types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from bot_body.database.models import save_user, get_site_user_id
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from standart_run import bot
from decouple import config
import requests

user_router = Router()

'''
class Register(StatesGroup):
    waiting_for_user_id = State()
'''
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    args = message.get_args()
    if args:
        token = args.strip()
        try:
            response = requests.get(f"https://todolist29.pythonanywhere.com/api/telegram-auth/?token={token}")
            response.raise_for_status()
            site_user_id = response.json()['user_id']
            save_user(message.from_user.id, site_user_id)
            await message.answer("✅ Telegram успешно привязан к сайту!")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")
        else:
            await message.answer("Привет! Чтобы подключить Telegram, перейди по ссылке с сайта.")
'''   
@user_router.message_handler(state=Register.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Нужно ввести число. Попробуй снова.")
        return
    site_user_id = int(message.text)
    save_user(message.from_user.id, site_user_id)
    await message.answer("Готово! Теперь ты можешь получать свои задачи.\nЧтобы проверить состояние задач, введите команду - </check>")
    await state.finish()
'''
def get_overdue_tasks(site_user_id):
    try:
        response = requests.get(f'https://todolist29.pythonanywhere.com/api/overdue/?user_id={site_user_id}')
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []


@user_router.message(Command("check"))
async def cmd_ckeck_tasks(message: Message):
    telegram_id = message.from_user.id
    site_user_id = get_site_user_id(telegram_id)

    if not site_user_id:
        await message.answer("Ты не зарегистрирован. Напиши /start")
        return

    tasks = get_overdue_tasks(site_user_id=site_user_id)

    if tasks:
        message = "🔔 Просроченные задачи:\n\n"
        for task in tasks:
            message += f"• {task['title']} (до {task['deadline']})\n"
    else:
        message = "✅ Нет просроченных задач"

    await bot.send_message(chat_id=telegram_id, text=message)