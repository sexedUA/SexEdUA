from aiogram.types import KeyboardButton, InlineKeyboardButton

talk = KeyboardButton('Поговоримо про секс? 🔥')
quiz = KeyboardButton('Квізи для дорослих 😻')
story = KeyboardButton('Sex Stories 😜')
kamasutra = KeyboardButton('KAMACУТРА 💏')
therapy = KeyboardButton('Sex Therapy 💆‍♀️')
subscribe = KeyboardButton('Підписатись на щоденний контент 🔔')
need_help = KeyboardButton('Допомога ℹ️')


vibrator_quiz = InlineKeyboardButton(
    text="Який вібратор тобі підходить 📝", callback_data='vibrator_quiz')

next_question = InlineKeyboardButton(
    text="Наступне питання", callback_data='next_question')


vibrator_q1 = [
    InlineKeyboardButton(text="Cтимуляція клітора", callback_data='q2'),
    InlineKeyboardButton(text="Вагінальне проникнення", callback_data='q2'),
    InlineKeyboardButton(
        text="Не можу обрати між першим і другим", callback_data='q2'),
    InlineKeyboardButton(
        text="Не знаю, але хочу дізнатися", callback_data='q2'),
]
