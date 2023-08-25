from aiogram import types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database import database as db


def create_markup(links: list):

    links_markup = InlineKeyboardMarkup(row_width=2)
    if links:
        for link in links:
            desc, url = link
            links_markup.add(InlineKeyboardButton(desc, url=url))

    subscribe_link = db.get_link_subcribe()
    desc, link = subscribe_link
    links_markup.add(InlineKeyboardButton(desc, link))
    return links_markup


async def talk_handler(message: types.Message):
    links = db.get_link()
    links_markup = create_markup(links)
    await message.answer("""У цьому розділі ми пропонуємо тобі переглянути відео на цікаві теми. У нас є багато корисного про відносини, здоров'я та задоволення.
Підписуйтесь на канал, щоб нормально практикувати з LOVESPACE.""")
    await message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)


# async def next_prev_handler(callback: types.CallbackQuery, start: int):
#     if callback.data == 'next_link':
#         links = db.get_link()
#         start += 3
#         links = links[start:start+3]
#         if len(links) < 1:
#             links_markup = InlineKeyboardMarkup(
#                 row_width=2).add(end_link).add(back_to_main)
#             await callback.message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)
#             return 0
#         else:
#             links_markup = create_markup(links)
#         await callback.message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)
#         return start
#     if callback.data == 'prev_link':
#         start -= 3
#         if start < 0:
#             links_markup = InlineKeyboardMarkup(
#                 row_width=2).add(end_link).add(back_to_main)
#             await callback.message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)
#             return 0
#         links_markup = create_markup(start)
#         await callback.message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=links_markup)
#         return start
