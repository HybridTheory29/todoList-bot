import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from decouple import config


bot = Bot(token=config("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

async def main():
    from bot_body.handlers import user_router
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())