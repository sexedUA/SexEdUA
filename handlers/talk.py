from aiogram import types
from keyboards.keyboards import talk_markup


async def talk_handler(message: types.Message):
    await message.answer("У цьому розділі ми пропонуємо тобі переглянути відео на цікаві теми. У нас є багато корисного про відносини, здоров'я та задоволення.Підписуйтесь на канал, щоб нормально практикувати з LOVESPACE.")
    await message.answer('_Обери тему яку хочеш дослідити_', parse_mode='Markdown', reply_markup=talk_markup)
