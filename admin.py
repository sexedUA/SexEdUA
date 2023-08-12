from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import random
import os
import sqlite3 as sq

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("ADMIN_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print("Бот запрацював!")


class NewOrder(StatesGroup):
    desc = State()
    photo = State()


class NewReview(StatesGroup):
    desc = State()
    photo = State()
    link = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id == int(os.getenv("ADMIN_ID1")) or message.from_user.id == int(os.getenv("ADMIN_ID2")):
        await message.answer("Привіт, Адмін. Над чим попрацюємо сьогодні?", reply_markup=kb.main_menu_admin)

@dp.message_handler(text="Назад", state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if (current_state == "NewOrder.desc") or (current_state == "NewOrder.photo"):
        await state.finish() 
        await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?",reply_markup=kb.main_menu_admin)
    await state.finish()
    await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?",reply_markup=kb.main_menu_admin)


@dp.message_handler(text="Поза дня")
async def add_item(message: types.Message):
    await message.answer("Потрібно додати опис пози", reply_markup=kb.cancel)
    await NewOrder.desc.set()

@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
    await message.answer("Додайте фото чи GIF")
    await state.set_state(NewOrder.photo)


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_content_check(message: types.Message):
    await message.answer('Це не фото і не гіф!')


@dp.message_handler(content_types=[types.ContentType.ANIMATION], state=NewOrder.photo)
async def add_item_animation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        file_path = await bot.get_file(message.animation.file_id)
        animation_file = await bot.download_file(file_path.file_path)
        animation_bytes = animation_file.read()
        data['photo'] = animation_bytes
    await db.add_item(state)
    await message.answer("Поза додана!", reply_markup=kb.main_menu_admin)
    await state.finish()


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer("Поза додана!", reply_markup=kb.main_menu_admin)
    await state.finish()

@dp.message_handler(text="Додати ревью на товар")
async def add_item(message: types.Message):
    await message.answer("Потрібно додати текст ревью", reply_markup=kb.cancel)
    await NewReview.desc.set()

@dp.message_handler(state=NewReview.desc)
async def add_review_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
    await message.answer("Додайте лінк на товар з магазину")
    await NewReview.link.set()

@dp.message_handler(state=NewReview.link)
async def add_review_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text
    await message.answer("Додайте фото товару")
    await NewReview.photo.set()


@dp.message_handler(lambda message: not message.photo, state=NewReview.photo)
async def add_review_content_check(message: types.Message):
    await message.answer('Це не фото :(')

@dp.message_handler(content_types=[types.ContentType.PHOTO], state=NewReview.photo)
async def add_review_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        photo_obj = message.photo[-1]  # Виберіть перший об'єкт фотографії зі списку
        file_path = await bot.get_file(photo_obj.file_id)
        photo_file = await bot.download_file(file_path.file_path)
        photo_bytes = photo_file.read()
        data['photo'] = photo_bytes
    await db.add_review(state)
    await message.answer("Огляд товару доданий!", reply_markup=kb.main_menu_admin)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
