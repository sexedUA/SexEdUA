from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import os


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("ADMIN_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)


async def set_default_commands(dp):
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню"),
        types.BotCommand("cancel", "Вийти")
    ]
    await bot.set_my_commands(commands)
    print("Бот запрацював!")


async def on_shutdown(dp):
    await db.db_close()


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
        await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?", reply_markup=kb.main_menu_admin)
    await state.finish()
    await message.answer("Ви вийшли з поточного стану. Що б ви хотіли робити далі?", reply_markup=kb.main_menu_admin)


@dp.message_handler(commands=["menu"])
async def menu_handler(message: types.Message):
    await message.answer("Вибери над чим будеш працювати", reply_markup=kb.main_menu_admin)


@dp.message_handler(text='Секс-історія')
async def get_stories(message: types.Message):
    stories = db.get_stories_admin()
    if stories:
        pass
    else:
        await message.answer("Нових історій не знайдено 😔")


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
async def add_review_text(message: types.Message):
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
        # Виберіть перший об'єкт фотографії зі списку
        photo_obj = message.photo[-1]
        file_path = await bot.get_file(photo_obj.file_id)
        photo_file = await bot.download_file(file_path.file_path)
        photo_bytes = photo_file.read()
        data['photo'] = photo_bytes
    await db.add_review(state)
    await message.answer("Огляд товару доданий!", reply_markup=kb.main_menu_admin)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(
        dp, on_startup=set_default_commands, skip_updates=True, on_shutdown=on_shutdown)
