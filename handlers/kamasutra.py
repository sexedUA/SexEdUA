from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import random
import os
import time
import io
from handlers.menu import quiz_handler
from handlers.quiz import quiz_choose_handler
from handlers.story import story_handler, read_story, add_story, Story

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
quiz_score = []


async def show_animation(chat_id, animation_bytes, caption, reply_markup=None):
    if isinstance(animation_bytes, str):
        animation_bytes = animation_bytes.encode()
    animation_io = io.BytesIO(animation_bytes)
    await bot.send_video(chat_id=chat_id, video=types.InputFile(animation_io, filename='animation.gif'), caption=caption, reply_markup=reply_markup)

async def positions(message: types.Message):
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