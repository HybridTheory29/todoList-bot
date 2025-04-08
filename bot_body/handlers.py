from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Этот бот будет присылать тебе уведомления о просроченных заданиях на сайте ToDo-List')
    #интегрировать в текст ToDo-List ссылку на сайт