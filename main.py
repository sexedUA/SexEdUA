from aiogram import Bot, Dispatcher, executor, types
from app import keyboards as kb
from app import database as db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.environ.get("TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()
    print("work")


class new_position(StatesGroup):
    name = State()
    description = State()
    photo = State()


@dp.message_handler(commands=["start"])
async def start_bot(
    message: types.Message,
):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer("You are signed as admin", reply_markup=kb.admin_panel)
    else:
        await message.answer("I don't understand")


@dp.message_handler(commands=["kamasutra"])
async def start_bot(
    message: types.Message,
):
    await message.answer("Choose cathegory", reply_markup=kb.kamasutra)


@dp.message_handler(text="admin")
async def start_bot(
    message: types.Message,
):
    await message.answer("Successfully", reply_markup=kb.admin_panel)


@dp.message_handler(text="Oral")
async def start_bot(
    message: types.Message,
):
    await message.answer("Choose cathegory", reply_markup=kb.kamasutra_Oral)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
