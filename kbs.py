from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_client = InlineKeyboardMarkup(resize_keyboard=True)
introduction = InlineKeyboardMarkup('Знайомство',
                                    callback_data='Знайомство')
yes_key = InlineKeyboardButton('Так', callback_data='так')
no_key = InlineKeyboardButton('Ні')

b1 = kb_client.row(introduction)
b2 = kb_client.row(yes_key, no_key)
