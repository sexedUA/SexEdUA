import os
from aiogram import Bot, Dispatcher, executor, types
from handlers.menu import menu_handler


BOT_TOKEN = os.environ.get("BOT_TOKEN")


def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['menu'])
    async def menu(message: types.Message):
        await menu_handler(message=message)

    executor.start_polling(dp)


if __name__ == '__main__':
    main()
