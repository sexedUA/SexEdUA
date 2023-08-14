from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import keyboards as kb
from database import database as db
from dotenv import load_dotenv
import random
import os
import io


async def show_photo(chat_id, photo_data, caption, reply_markup=None):
    # if photo_data["file_id"] is not None:
    #     await bot.send_photo(chat_id=chat_id, photo=photo_data["file_id"], caption=caption, reply_markup=kb.main_menu)
    # else:
    if "photo" in photo_data:  # Проверяем наличие фото в photo_data
        photo_io = io.BytesIO(photo_data["photo"])
        photo_io.name = 'photo.jpg'
        input_photo = types.InputFile(photo_io)
        await bot.send_photo(chat_id=chat_id, photo=input_photo, caption=caption, reply_markup=kb.main_menu)
        # file_id = response.photo[-1].file_id
        # Сохраняем полученный file_id в photo_data
        # photo_data["file_id"] = file_id
        # connection = sq.connect("kamasutra.db")
        # cur = connection.cursor()
        # cur.execute("UPDATE reviews SET file_id = ? WHERE id = ?",
        #             (file_id, photo_data["id"]))
        # connection.commit()
        # connection.close()

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
quiz_score = []


async def send_review(message: types.Message):
    reviews = db.get_review()
    if reviews:
        review = random.choice(reviews)
        id, desc, link, photo = review
        photo_data = {
            "id": id,
            "photo": photo,
        }
        max_caption_length = 1000
        if len(desc) > max_caption_length:
            desc = desc[:max_caption_length]
        await show_photo(message.chat.id, photo_data, caption=desc)
        await message.answer(f"Придбати цей товар можеш тут: {link}")
    else:
        await message.reply("Немає доступних оглядів :( ")
