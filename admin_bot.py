from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook

from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import os
import logging

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME_ADMIN")


# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080

# webhook settings
WEBHOOK_HOST = RENDER_EXTERNAL_HOSTNAME
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("ADMIN_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    commands = [
        types.BotCommand("start", "Почати"),
        types.BotCommand("menu", "Головне меню"),
        types.BotCommand("cancel", "Вийти"),
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


class NewLink(StatesGroup):
    description = State()
    link = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id == int(
        os.getenv("ADMIN_ID1")
    ) or message.from_user.id == int(os.getenv("ADMIN_ID2")):
        await message.answer(
            "Привіт, Адмін. Над чим попрацюємо сьогодні?",
            reply_markup=kb.main_menu_admin,
        )


@dp.message_handler(text="Назад", state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if (current_state == "NewOrder.desc") or (current_state == "NewOrder.photo"):
        await state.finish()
        await message.answer(
            "Ви вийшли з поточного стану. Що б ви хотіли робити далі?",
            reply_markup=kb.main_menu_admin,
        )
    await state.finish()
    await message.answer(
        "Ви вийшли з поточного стану. Що б ви хотіли робити далі?",
        reply_markup=kb.main_menu_admin,
    )


@dp.message_handler(commands=["menu"])
async def menu_handler(message: types.Message):
    await message.answer(
        "Вибери над чим будеш працювати", reply_markup=kb.main_menu_admin
    )


@dp.message_handler(text="Секс-історія")
async def get_stories(message: types.Message):
    stories = db.get_stories_admin()
    if stories:
        story = stories.pop(0)
        id, text, status = story
        await message.answer(text=text, reply_markup=kb.story_markup_admin)
    else:
        await message.answer("Нових історій не знайдено 😔")


@dp.message_handler(text="Наступна історія")
async def next_story(message: types.Message):
    stories = db.get_stories_admin()
    if stories:
        story = stories.pop(0)
        id, text, status = story
        await message.answer(text=text, reply_markup=kb.story_markup_admin)
    else:
        await message.answer("Нових історій не знайдено 😔")


@dp.callback_query_handler(
    lambda query: query.data in ["approve-story", "delete-story"]
)
async def story_query(callback_query: types.CallbackQuery):
    (story_id,) = db.get_story_by_text(callback_query.message.text).pop(0)
    db.update_story(story_id, callback_query.data)
    answer = (
        "Історія додана"
        if callback_query.data == "approve-story"
        else "Історія видалена"
    )
    await callback_query.message.answer(text=answer, reply_markup=kb.next_story_markup)


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
            chat_id=callback_query.from_user.id, text="Оберіть тип контенту"
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
    await message.answer("Це не фото і не гіф!")


@dp.message_handler(content_types=[types.ContentType.ANIMATION], state=NewOrder.photo)
async def add_item_animation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        file_path = await bot.get_file(message.animation.file_id)
        animation_file = await bot.download_file(file_path.file_path)
        animation_bytes = animation_file.read()
        data["photo"] = animation_bytes
    await db.add_item(state)
    await message.answer("Поза додана!", reply_markup=kb.main_menu_admin)
    await state.finish()


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
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
    await message.answer("Це не фото :(")


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=NewReview.photo)
async def add_review_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Виберіть перший об'єкт фотографії зі списку
        photo_obj = message.photo[-1]
        file_path = await bot.get_file(photo_obj.file_id)
        photo_file = await bot.download_file(file_path.file_path)
        photo_bytes = photo_file.read()
        data["photo"] = photo_bytes
    await db.add_review(state)
    await message.answer("Огляд товару доданий!", reply_markup=kb.main_menu_admin)
    await state.finish()


@dp.message_handler(text="Додати посилання на YouTube")
async def add_link_handler(message: types.Message):
    await message.answer("Потрібно додати опис відео", reply_markup=kb.cancel)
    await NewLink.description.set()


@dp.message_handler(state=NewLink.description)
async def add_link_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await message.answer("Додайте лінк на відео з YouTube")
    await NewLink.link.set()


@dp.message_handler(state=NewLink.link)
async def add_video_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text
    await db.add_link(state)
    await message.answer("Посилання додане!", reply_markup=kb.main_menu_admin)
    await state.finish()


@dp.message_handler(text="Переглянути заявки на консультацію")
async def view_consultation_requests(message: types.Message):
    consultation_requests = db.get_consultation_requests()

    if consultation_requests:
        response = ""
        for phone, status in consultation_requests:
            if not status:
                response += f"Phone: {phone}\n"

        if response:
            keyboard = types.ReplyKeyboardMarkup(
                row_width=1, resize_keyboard=True)
            keyboard.add("Переглянуто", "Вийти")

            await message.answer(
                f"Список заявок на консультацію зі статусом 'Не переглянуто':\n{response}",
                reply_markup=keyboard,
            )
        else:
            await message.answer("Всі заявки вже переглянуті.")
    else:
        await message.answer("Немає заявок на консультацію")


@dp.message_handler(text="Переглянуто")
async def mark_consultation_viewed(message: types.Message):
    consultation_requests = db.get_consultation_requests()

    for phone, status in consultation_requests:
        if not status:
            await db.update_consultation_status(
                phone, True
            )  # Добавляем await перед функцией

    await message.answer("Статуси заявок на консультацію змінено на 'Переглянуто'.")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    # executor.start_polling(
    #     dp, on_startup=on_startup, skip_updates=True, on_shutdown=on_shutdown
    # )
