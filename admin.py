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


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)  # записує в бд id користувача
    if message.from_user.id == int(os.getenv("ADMIN_ID1")) or message.from_user.id == int(os.getenv("ADMIN_ID2")):
        await message.answer("Привіт, Адмін", reply_markup=kb.main_menu_admin)


@dp.message_handler(text="Редагувати")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer("Ви зайшли як адмін", reply_markup=kb.adminpanel)
    else:
        await message.reply("Не розумію.")


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == "add":
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Оберіть тип контенту"
        )
    elif callback_query.data == "delete":
        await bot.send_message(
            chat_id=callback_query.from_user.id, text="Вы видаляєте контент"
        )
    elif callback_query.data == "mail":
        await bot.send_message(
            chat_id=callback_query.from_user.id, text="Вы хочете зробити розсилку"
        )


@dp.message_handler(text="Поза дня")
async def add_item(message: types.Message):
    await message.answer("Потрібно додати опис пози", reply_markup=kb.cancel)
    await NewOrder.desc.set()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
        print(data["desc"])
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


# @dp.message_handler(lambda message: not message.text, state=NewOrder.photo)
# async def add_item_content_check(message: types.Message):
#     await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
