from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import random
import os
import io


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)

async def set_default_commands(dp):
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню")
    ]
    await bot.set_my_commands(commands)
    await db.db_start()
    print("Бот запрацював!")


class NewOrder(StatesGroup):
    desc = State()
    photo = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)  # записує в бд id користувача
    await message.answer(
        "Привіт!",
        reply_markup=kb.main_menu,
    )
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    await message.answer("Виберіть розділ", reply_markup=kb.main_menu)


async def show_animation(chat_id, animation_bytes, caption, reply_markup=None):
    if isinstance(animation_bytes, str):
        animation_bytes = animation_bytes.encode()
    animation_io = io.BytesIO(animation_bytes)
    await bot.send_video(chat_id=chat_id, video=types.InputFile(animation_io, filename='animation.gif'), caption=caption, reply_markup=reply_markup)

@dp.message_handler(text="ПОЗА ДНЯ😏")
async def cmd_katalog(message: types.Message):
    positions = db.get_positions()
    if positions:
        random_position = random.choice(positions)
        pos_id, pos_desc, pos_photo = random_position
        max_caption_length = 1000
        if len(pos_desc) > max_caption_length:
            pos_desc = pos_desc[:max_caption_length]
        response = f"Така поза: {pos_desc}"
        await show_animation(message.chat.id, pos_photo, caption=response, reply_markup=kb.main_menu)
    else:
        await message.reply("Немає доступних поз")



@dp.message_handler(commands=["id"])
async def cmd_id(message: types.Message):
    await message.answer(f"{message.from_user.id}")


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Я тебе не розумію 😔")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup = set_default_commands, skip_updates=True)


        
        
            