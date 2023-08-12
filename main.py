from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
import asyncio
import aiohttp
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
from handlers.greetings import start_on, cancel_handler, invalid_age, greetings, get_age, get_gender, get_orientation
from handlers.kamasutra import show_animation, positions
from handlers.reviews import show_photo, send_review
from handlers.talk import talk_handler
from bs4 import BeautifulSoup
import sqlite3 as sq


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
quiz_score = []


class Greetings(StatesGroup):
    age = State()
    gender = State()
    orientation = State()


async def set_default_commands(dp):
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню"),
        types.BotCommand("cancel", "Вийти")
    ]
    await bot.set_my_commands(commands)
    await db.db_start()
    print("Бот запрацював!")


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await start_on(message)


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await cancel_handler(message, state)


@dp.callback_query_handler(lambda query: query.data in ["yes", "no"])
async def greetings_start(callback_query: types.CallbackQuery, state: FSMContext):
    await greetings(callback_query, state)


@dp.message_handler(lambda message: not message.text.isdigit(), state=Greetings.age)
async def invalid_age_(message: types.Message):
    await invalid_age(message)


@dp.message_handler(lambda message: message.text.isdigit(), state=Greetings.age)
async def get_age_(message: types.Message, state: FSMContext):
    await get_age(message, state)


@dp.callback_query_handler(lambda query: query.data in ["woman", "man"], state=Greetings.gender)
async def get_gender_(callback_query: types.CallbackQuery, state: FSMContext):
    await get_gender(callback_query, state)


@dp.callback_query_handler(lambda query: query.data in ["hetero", "homo", "bi"], state=Greetings.orientation)
async def get_orientation_(callback_query: types.CallbackQuery, state: FSMContext):
    await get_orientation(callback_query, state)


@dp.message_handler(text="Відкрий скарбничку з іграшками 🧸")
async def send_review_(message: types.Message):
    await send_review(message)


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    await message.answer("Виберіть розділ", reply_markup=kb.main_menu)


@dp.message_handler(text="ПОЗА ДНЯ😏")
async def positions_(message: types.Message):
    await positions(message)


@dp.message_handler(commands=["id"])
async def cmd_id(message: types.Message):
    await message.answer(f"{message.from_user.id}")


@dp.message_handler(text="Sex Stories 😜")
async def random_story(message: types.Message):
    await story_handler(message)


@dp.message_handler(text="Квізи для дорослих 😻")
async def quiz_chose(message: types.Message):
    await quiz_handler(message)


@dp.callback_query_handler(text='read_story')
async def read_handler(callback: types.CallbackQuery):
    await read_story(callback)


@dp.callback_query_handler(text='add_story')
async def add_handler(callback: types.CallbackQuery):
    await add_story(callback)


@dp.message_handler(state=Story.text)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await db.add_story(state)
    await message.answer("Історія додана! Скоро вона стане доступною для усіх")
    await state.finish()


@dp.callback_query_handler(lambda query: query.data in ['vibrator_quiz'] or query.data.startswith('quiz'))
async def quiz_callback(callback: types.CallbackQuery):
    global quiz_score
    quiz_score = await quiz_choose_handler(callback, quiz_score)


@dp.message_handler(text="Поговоримо про секс?")
async def talk(message: types.Message):
    await talk_handler(message)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Я тебе не розумію 😔")

if __name__ == "__main__":
    executor.start_polling(
        dp, on_startup=set_default_commands, skip_updates=True)
