from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

kamasutra = ReplyKeyboardMarkup(resize_keyboard=True)
kamasutra.add("Oral", "Face to Face").add("Real Entry", "Butterfly Variations").add(
    "Cowgirl Variations", "Exotic"
)


kamasutra_Oral = InlineKeyboardMarkup(row_width=2)
kamasutra_Oral.add(
    InlineKeyboardButton(text="69 Classic", callback_data="name"),
    InlineKeyboardButton(text="69 Sitting", callback_data="description"),
    InlineKeyboardButton(text="Plumber", callback_data="photo"),
)

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add("add_position")
