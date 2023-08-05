import os
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from kbs import b1, b2

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    welcome_text = """
    🌟 **Щирі вітання!**🌟
    Це бот-простір LOVESPACE. Створений для пізнання себе,
    своїх почуттів та експериментів.
    🚀Наша місія - формування секс-культури та цінностей в Україні. 🚀
    """
    await message.answer(welcome_text, reply_markup=b1)


@dp.message_handler(lambda c: c.data == 'b1')
async def b1_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await introduction_message(callback_query.message)


async def introduction_message(message: types.Message):
    welcome_text2 = """
        До того як ми почнемо, мені необхідно трохи
        більше інформації, щоб підібрати контент саме для
        тебе. Не хвилюйся, це не займе багато часу.
        Я почекаю⏳
        """

    await message.answer(welcome_text2, reply_markup=b2)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
