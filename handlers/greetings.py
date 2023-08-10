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
from handlers.menu import quiz_handler
from handlers.quiz import quiz_choose_handler
from handlers.story import story_handler, read_story, add_story, Story

storage = MemoryStorage()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot,storage=storage)

class Greetings(StatesGroup):
    age = State()
    gender = State()
    orientation = State()


async def start_on(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id) 
    if not user:
        await message.answer("Привіт!")
        await message.answer_sticker('CAACAgIAAxkBAAIMvGTTY5ISyIjn-N6yi2VILV1sBmPbAAITDAAC4stASAoWS8U3wbIyMAQ')
        time.sleep(1)
        await message.answer("Давай познайомимось?😉", reply_markup=kb.greetings)
    else:
        await message.answer("Привітики 🥰 Що обереш сьогодні?", reply_markup=kb.main_menu)



async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if (current_state == "Greetings.age") or (current_state == "Greetings.gender") or (current_state == "Greetings.orientation"):
        await state.finish() 
        await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?")
    await state.finish()
    await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?")


async def greetings(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        # await bot.send_sticker(CAACAgEAAxkBAAIMwmTTZWvfNF2Xp4km4bVALTxERw-9AALRAQACOA6CEYhFy3sr91pVMAQ)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Скільки тобі років?")
        await Greetings.age.set()
    elif callback_query.data == "no":
        # await bot.send_sticker('CAACAgIAAxkBAAIMv2TTY7uFZwFDOkfkU0FVyBRaHcs5AAJ5DAACoa5ASNb10Q3I2CyMMAQ')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Тоді познайомимся пізніше😉. Дивись що у нас є в меню ⬇️ ", reply_markup=kb.main_menu)
        

async def invalid_age(message: types.Message):
    await message.answer("Введіть будь ласка числове значення вашого віку.")
    

async def get_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    if age < 18:
        await state.finish()
        await message.answer("🔞 На жаль, наш контент має обмеження 18+.", reply_markup=kb.main_menu)
        return 
    await state.update_data(age=age)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Укажи свій гендер:",
                           reply_markup=kb.gender_keyboard
                           )
    await Greetings.next()



async def get_gender(query: types.CallbackQuery, state: FSMContext):
    gender = query.data
    await state.update_data(gender=gender)
    await bot.send_message(chat_id=query.from_user.id,
                           text="Укажи свою орієнтацію:",
                           reply_markup=kb.orientation_keyboard
                           )
    await Greetings.next()


async def get_orientation(query: types.CallbackQuery, state: FSMContext):
    orientation = query.data
    async with state.proxy() as data:
        age = data["age"]
        gender = data["gender"]
        data["orientation"] = orientation
    await db.cmd_start_db(query.from_user.id, age, gender, orientation) 
    await bot.send_message(chat_id=query.from_user.id,
                           text="Дякуємо😊 Приємного перегляду. Рекомендуємо обрату улюблену позу у рубриці **Поза дня**",reply_markup=kb.main_menu
                           )
    await state.finish()

