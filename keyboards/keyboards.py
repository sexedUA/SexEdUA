from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


talk = KeyboardButton("Поговоримо про секс? ")
quiz = KeyboardButton("Квізи для дорослих 😻")
story = KeyboardButton("Sex Stories 😜")
kamasutra = KeyboardButton("ПОЗА ДНЯ😏")
therapy = KeyboardButton("Sex Therapy 💆‍♀️")
subscribe = KeyboardButton("Підписатись на щоденний контент 🔔")
need_help = KeyboardButton("Допомога ℹ️")

main_menu = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[[talk], [quiz, story], [kamasutra, therapy], [subscribe], [need_help]],
)

greetings = InlineKeyboardMarkup(row_width=2)
greetings.add(
    InlineKeyboardButton(text="Давай 😊 ", callback_data="yes"),
    InlineKeyboardButton(text="Пізніше 👌 ", callback_data="no"),
)

gender_keyboard = InlineKeyboardMarkup(row_width=2)
gender_keyboard.add(
    InlineKeyboardButton(text="Жінка ", callback_data="woman"),
    InlineKeyboardButton(text="Чоловік ", callback_data="man"),
)

orientation_keyboard =  InlineKeyboardMarkup(row_width=1)
orientation_keyboard.add(
    InlineKeyboardButton(text="Гетеросексуал", callback_data="hetero"),
    InlineKeyboardButton(text="Гомосексуал", callback_data="homo"),
    InlineKeyboardButton(text="Бісексуал", callback_data="bi")
)


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

main_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_admin.add('Поза дня').add('Секс-історія').add('Секс-шоп')


adminpanel = InlineKeyboardMarkup(row_width=1)
adminpanel.add(
    InlineKeyboardButton(text="Додати контент", callback_data="add"),
    InlineKeyboardButton(text="Видалити контент", callback_data="delete"),
    InlineKeyboardButton(text="Зробити розсилку", callback_data="mail"),
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add("Отмена")