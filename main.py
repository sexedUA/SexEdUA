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


async def set_default_commands(dp):
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню")
    ]
    await bot.set_my_commands(commands)
    await db.db_start()
    print("Бот запрацював!")


class Greetings(StatesGroup):
    age = State()
    gender = State()
    orientation = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт!"
    )
    await message.answer_sticker('CAACAgIAAxkBAAIMvGTTY5ISyIjn-N6yi2VILV1sBmPbAAITDAAC4stASAoWS8U3wbIyMAQ')
    time.sleep(1)
    await message.answer(
        "Давай познайомимось?😉", reply_markup=kb.greetings)


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        # await bot.send_sticker(CAACAgEAAxkBAAIMwmTTZWvfNF2Xp4km4bVALTxERw-9AALRAQACOA6CEYhFy3sr91pVMAQ)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Скільки тобі років?")
        await Greetings.age.set()
    elif callback_query.data == "no":
        # await bot.send_sticker('CAACAgIAAxkBAAIMv2TTY7uFZwFDOkfkU0FVyBRaHcs5AAJ5DAACoa5ASNb10Q3I2CyMMAQ')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Тоді познайомимся пізніше😉. Дивись що у нас є в меню ⬇️ ", reply_markup=kb.main_menu)


@dp.message_handler(lambda message: message.text.isdigit(), state=Greetings.age)
async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    # if age<18:

    await state.update_data(age=age)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Укажи свій гендер:",
                           reply_markup=kb.gender_keyboard
                           )
    await Greetings.next()


@dp.callback_query_handler(lambda query: query.data in ["woman", "man"], state=Greetings.gender)
async def get_gender(query: types.CallbackQuery, state: FSMContext):
    gender = query.data
    await state.update_data(gender=gender)
    await bot.send_message(chat_id=query.from_user.id,
                           text="Укажи свою орієнтацію:",
                           reply_markup=kb.orientation_keyboard
                           )
    await Greetings.next()


@dp.callback_query_handler(lambda query: query.data in ["hetero", "homo", "bi"], state=Greetings.orientation)
async def get_orientation(query: types.CallbackQuery, state: FSMContext):
    orientation = query.data
    async with state.proxy() as data:
        age = data["age"]
        gender = data["gender"]
    await db.cmd_start_db(query.from_user.id, age, gender, orientation)
    await bot.send_message(chat_id=query.from_user.id,
                           text="Дякуємо😊"
                           )
    await state.finish()


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


# @dp.message_handler()
# async def answer(message: types.Message):
#     await message.reply("Я тебе не розумію 😔")
@dp.message_handler(text="Sex Stories 😜")
async def random_story(message: types.Message):
    await story_handler(message)


@dp.message_handler(text="Квізи для дорослих 😻")
async def quiz_chose(message: types.Message):
    await quiz_handler(message)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Я тебе не розумію 😔")


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


@dp.callback_query_handler()
async def quiz_callback(callback: types.CallbackQuery):
    global quiz_score
    quiz_score = await quiz_choose_handler(callback, quiz_score)


if __name__ == "__main__":
    executor.start_polling(
        dp, on_startup=set_default_commands, skip_updates=True)
