import os
from aiogram import Bot, Dispatcher, executor, types
from handlers.menu import menu_handler, quiz_handler

from handlers.quiz import quiz_choose_handler


BOT_TOKEN = os.environ.get("BOT_TOKEN")


def updating_answers(poll_id, user_id, answer_ids, answers: dict):
    if user_id in answers:
        answer_list = answers[user_id]['answer_ids']
        answers[user_id].update(
            {'pool_id': poll_id, 'answer_ids': answer_list.append(answer_ids)})
    else:
        answers[user_id] = {'pool_id': poll_id,
                            'answer_ids': [answer_ids]}


def main():

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(bot)

    async def set_default_commands(dp):
        commands = [
            types.BotCommand("start", "Почати"),
            types.BotCommand("menu", "Головне меню"),
        ]
        await bot.set_my_commands(commands)

    @dp.message_handler(commands=['menu'])
    async def menu(message: types.Message):
        await menu_handler(message=message)

    @dp.message_handler()
    async def quiz(message: types.Message):
        await quiz_handler(message)

    @dp.callback_query_handler()
    async def quiz_callback(callback: types.CallbackQuery, ):
        await quiz_choose_handler(callback)

    # @dp.poll_answer_handler()
    # async def poll_answer(poll_answer: types.PollAnswer):
    #     answer_ids = poll_answer.option_ids  # list of answers
    #     user_id = poll_answer.user.id
    #     poll_id = poll_answer.poll_id
    #     updating_answers(poll_id, user_id, answer_ids, answers)
    #     print(answers)

    executor.start_polling(dp, on_startup=set_default_commands)


if __name__ == '__main__':
    main()
