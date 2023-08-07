from aiogram import types
from keyboards.keyboards import next_question, vibrator_q1


next_markup = types.InlineKeyboardMarkup().add(next_question)

vibrator_quiz = {
    "question_1": ("Що тобі більше подобається?", ["Cтимуляція клітора", "Вагінальне проникнення", "Не можу обрати між першим і другим", "Не знаю, але хочу дізнатися"]),
    "question_2": ("Яке відчуття звучить для тебе найкраще?", ["Широка та гучна вібрація", "Інтенсивна, цілеспрямована стимуляція", "Ніжний дотик", "Все, що схоже на оральний секс"]),
    "question_3": ("Що тобі більше подобається?", ["Cтимуляція клітора", "Вагінальне проникнення", "Не можу обрати між першим і другим", "Не знаю, але хочу дізнатися"]),
    "question_4": ("Що тобі більше подобається?", ["Cтимуляція клітора", "Вагінальне проникнення", "Не можу обрати між першим і другим", "Не знаю, але хочу дізнатися"])
}

q1_markup = types.InlineKeyboardMarkup().add(vibrator_q1[0]).add(
    vibrator_q1[1]).add(vibrator_q1[2]).add(vibrator_q1[3])


async def quiz_choose_handler(callback: types.CallbackQuery):
    if callback.data == 'vibrator_quiz':
        await callback.message.answer_poll(vibrator_quiz["question_1"][0], vibrator_quiz["question_1"][1], reply_markup=next_markup, is_anonymous=False)
    if callback.data == 'next_question':
        await callback.message.answer_poll(vibrator_quiz["question_2"][0], vibrator_quiz["question_2"][1], reply_markup=next_markup, is_anonymous=False)

# async def quiz_choose_handler(callback: types.CallbackQuery):
#     if callback.data == 'vibrator_quiz':
#         await callback.message.answer("Що тобі більше подобається?", reply_markup=q1_markup)
#     if callback.data == 'q2':
#         print(callback)
