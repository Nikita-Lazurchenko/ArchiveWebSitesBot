import asyncio

from aiogram import Bot, Dispatcher
from application.handlers import router

async def main():
    bot = Bot(token='')
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
