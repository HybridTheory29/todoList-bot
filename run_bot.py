import logging
from aiohttp import web
from aiogram import Bot
from decouple import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config('BOT_TOKEN'))

routes = web.RouteTableDef()

@routes.post("/notify/")
async def notify(request):
    if request.headers.get("Authorization") != f"Bearer секрет":
        return web.Response(status=403, text="Forbidden")
    try:
        data = await request.json()
        title = data.get("title")
        deadline = data.get("deadline")

        if not title or not deadline:
            return web.Response(status=400, text="Missing title or deadline")

        message = f"🔔 Просрочена задача:\n\n• {title} (до {deadline})"
        await bot.send_message(config('CHAT_ID'), text=message)
        return web.Response(text="Message sent")

    except Exception as e:
        logging.error(f"Ошибка обработки запроса: {e}")
        return web.Response(status=500, text="Server error")

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)