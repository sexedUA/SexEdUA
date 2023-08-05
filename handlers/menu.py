from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message


talk = KeyboardButton('Поговоримо про секс? 🔥')
quiz = KeyboardButton('Квізи для дорослих 😻')
story = KeyboardButton('Sex Stories 😜')
kamasutra = KeyboardButton('KAMACУТРА 💏')
therapy = KeyboardButton('Sex Therapy 💆‍♀️')
subscribe = KeyboardButton('Підписатись на щоденний контент 🔔')
need_help = KeyboardButton('Допомога ℹ️')


menu_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, keyboard=[[talk], [quiz, story], [kamasutra, therapy], [subscribe], [need_help]])


async def menu_handler(message: Message):
    await message.answer("Виберіть розділ", reply_markup=menu_kb)
