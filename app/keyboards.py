from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

talk = KeyboardButton("Поговоримо про секс? 🔥")
quiz = KeyboardButton("Квізи для дорослих 😻")
story = KeyboardButton("Sex Stories 😜")
kamasutra = KeyboardButton("ПОЗА ДНЯ😏")
therapy = KeyboardButton("Sex Therapy 💆‍♀️")
subscribe = KeyboardButton("Підписатись на щоденний контент 🔔")
need_help = KeyboardButton("Допомога ℹ️")
adminpanel = KeyboardButton("Редагувати")

main_menu = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[[talk], [quiz, story], [kamasutra, therapy], [subscribe], [need_help]],
)

main_menu_admin = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [adminpanel],
    ],
)

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

