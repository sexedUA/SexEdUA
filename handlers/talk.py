from aiogram import types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database import database as db


def create_markup():
    links = db.get_link()
    print(links)


async def talk_handler(message: types.Message):
    links = db.get_link()
    links_markup = InlineKeyboardMarkup(row_width=1)
    if links:
        for link in links:
            id, desc, url = link
            links_markup.add(InlineKeyboardButton(desc, url=url))

    await message.answer("""У цьому розділі ми пропонуємо тобі переглянути відео на цікаві теми. У нас є багато корисного про відносини, здоров'я та задоволення.
Підписуйтесь на канал, щоб нормально практикувати з LOVESPACE.""")
    await message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)
