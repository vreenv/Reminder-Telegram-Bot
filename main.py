import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
import json


async def main():
    token = json.load(open("app/config/config.json"))['tg_token']
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('The bot is turned off')
