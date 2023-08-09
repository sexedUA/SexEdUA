from aiogram import types
from database import database as db
import random
from keyboards.keyboards import story_markup
from aiogram.dispatcher.filters.state import State, StatesGroup


class Story(StatesGroup):
    text = State()


async def story_handler(message: types.Message):
    await message.answer('У цьому розділі ти можеш прочитати історії людей, які поділились своїм вдалим і не дуже сексуальним досвідом. Або розказати усім про свій 🗣️', reply_markup=story_markup)


async def add_story(callback: types.CallbackQuery):
    await callback.message.answer("Напиши свою історію ✍️")
    await Story.text.set()


async def read_story(callback: types.CallbackQuery):
    stories = db.get_stories()
    if stories:
        story = random.choice(stories)
        _, story_text, status = story
        await callback.message.answer(f'_{story_text}_', parse_mode='Markdown', reply_markup=story_markup)
