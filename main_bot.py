from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import os
from handlers.menu import quiz_handler
from handlers.quiz import quiz_choose_handler
from handlers.story import story_handler, read_story, add_story, Story
from handlers.greetings import (
    start_on,
    cancel_handler,
    invalid_age,
    greetings,
    get_age,
    get_gender,
    get_orientation,
)
from handlers.kamasutra import positions
from handlers.reviews import send_review
from handlers.talk import talk_handler

import asyncio
import datetime

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
quiz_score = []
start_link: int = 0


class Greetings(StatesGroup):
    age = State()
    gender = State()
    orientation = State()


class Consulting(StatesGroup):
    waiting_for_phone = State()


async def set_default_commands(dp):
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню"),
        types.BotCommand("cancel", "Вийти"),
    ]
    description = 'Amazing bot'
    await bot.set_my_commands(commands)
    await bot.set_chat_description(description=description)
    print("Бот запрацював!")


async def on_shutdown(dp):
    await db.db_close()


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


@dp.callback_query_handler(
    lambda query: query.data in ["woman", "man"], state=Greetings.gender
)
async def get_gender_(callback_query: types.CallbackQuery, state: FSMContext):
    await get_gender(callback_query, state)


@dp.callback_query_handler(
    lambda query: query.data in ["hetero", "homo", "bi"], state=Greetings.orientation
)
async def get_orientation_(callback_query: types.CallbackQuery, state: FSMContext):
    await get_orientation(callback_query, state)


@dp.message_handler(text="Відкрий скарбничку з іграшками 🧸")
async def send_review_(message: types.Message):
    await send_review(message)


@dp.message_handler(commands=["menu"])
async def menu(message: types.Message):
    await message.answer("Виберіть розділ", reply_markup=kb.main_menu)


@dp.message_handler(text="ПОЗА ДНЯ😏")
async def positions_(message: types.Message):
    await positions(message.from_user.id)


@dp.message_handler(commands=["id"])
async def cmd_id(message: types.Message):
    await message.answer(f"{message.from_user.id}")


@dp.message_handler(text="Sex Stories 😜")
async def random_story(message: types.Message):
    await story_handler(message)


@dp.message_handler(text="Квізи для дорослих 😻")
async def quiz_chose(message: types.Message):
    await quiz_handler(message)


@dp.callback_query_handler(text="read_story")
async def read_handler(callback: types.CallbackQuery):
    await read_story(callback)


@dp.callback_query_handler(text="add_story")
async def add_handler(callback: types.CallbackQuery):
    await add_story(callback)


@dp.message_handler(state=Story.text)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await db.add_story(state)
    await message.answer("Історія додана! Скоро вона стане доступною для усіх", reply_markup=kb.story_markup)
    await state.finish()


@dp.callback_query_handler(
    lambda query: query.data in [
        "vibrator_quiz"] or query.data.startswith("quiz")
)
async def quiz_callback(callback: types.CallbackQuery):
    global quiz_score
    quiz_score = await quiz_choose_handler(callback, quiz_score)


@dp.message_handler(text="Поговоримо про секс?")
async def talk(message: types.Message):
    await talk_handler(message)


@dp.message_handler(text="Консультація з менеджером 📞")
async def consultation_start(message: types.Message):
    await message.answer("Введіть ваш номер телефону:")
    await Consulting.waiting_for_phone.set()


@dp.message_handler(state=Consulting.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
        await db.add_consultation(state, data["phone"])
        await message.answer(
            "Дякуємо, ваша консультація була зареєстрована! Наші менеджери скоро з вами зв'яжуться 😉"
        )
    await state.finish()


@dp.message_handler(text="Підписатись на щоденний контент 🔔")
async def subscribe_start(message: types.Message):
    await message.answer(
        "Пропонуємо підписатись на нас, щоб кожен день ми тобі відправляли щось цікавеньке 😉",
        reply_markup=kb.Subscr,
    )


@dp.message_handler(lambda message: message.text in ["Хочу ✅", "Пізніше ❌"])
async def subscribe_decision(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text == "Хочу ✅":
        await db.add_subscriber(user_id)  # Используем await здесь
        await message.answer("Дякуємо за підписку! 🎉")
    else:
        await message.answer("Будемо чекати тебе 😙")


async def send_positions_to_subscribers():
    subscribers = db.get_subscribers()  # Не используйте await здесь
    for subscriber_id in subscribers:
        await positions(subscriber_id)


async def schedule_positions():
    while True:
        await asyncio.sleep(60)  # Adjust interval as needed
        now = datetime.datetime.now()
        if now.hour == 10 and now.minute == 30:
            await send_positions_to_subscribers()
            await asyncio.sleep(60*60*24)  # Sleep for 24 hours


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Я тебе не розумію 😔")


def run_main_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_positions())
    executor.start_polling(dp, on_startup=set_default_commands,
                           skip_updates=True, on_shutdown=on_shutdown, loop=loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_positions())
    executor.start_polling(dp, on_startup=set_default_commands,
                           skip_updates=True, on_shutdown=on_shutdown, loop=loop)
