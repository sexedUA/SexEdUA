from aiogram.types import ReplyKeyboardMarkup, Message, InlineKeyboardMarkup

from keyboards.keyboards import (
    talk,
    quiz,
    story,
    kamasutra,
    therapy,
    subscribe,
    need_help,
    vibrator_quiz
)

menu_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, keyboard=[[talk], [quiz, story], [kamasutra, therapy], [subscribe], [need_help]])


quiz_ib = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[vibrator_quiz]])


async def menu_handler(message: Message):
    await message.answer("Виберіть розділ", reply_markup=menu_kb)


async def quiz_handler(message: Message):
    await message.answer('_"Виберіть квіз"_ ✍️', reply_markup=quiz_ib, parse_mode="Markdown")
