from aiogram import types
from keyboards.keyboards import vibrator_q1, vibrator_q2, vibrator_q3, vibrator_q4
import requests
from bs4 import BeautifulSoup
import random


def get_links(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    links = [el.get('href') for el in soup.find_all(
        'a', {"class": "product_card__title"})]
    return links


def get_random_link(links: list):
    return random.choice(links)


def create_question_markup(btns: list):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn in btns:
        markup.add(btn)
    return markup


q1_markup = create_question_markup(vibrator_q1)
q2_markup = create_question_markup(vibrator_q2)
q3_markup = create_question_markup(vibrator_q3)
q4_markup = create_question_markup(vibrator_q4)


async def quiz_choose_handler(callback: types.CallbackQuery, score: list):
    if callback.data == 'vibrator_quiz':
        await callback.message.answer('_"Що тобі більше подобається?"_', reply_markup=q1_markup, parse_mode='Markdown')
        return score
    if callback.data.startswith('quiz_q2'):
        score.append(callback.data)
        await callback.message.answer('_"Яке відчуття звучить для тебе найкраще?"_', reply_markup=q2_markup, parse_mode='Markdown')
        return score
    if callback.data.startswith('quiz_q3'):
        score.append(callback.data)
        await callback.message.answer('_"Скільки у тебе часу?"_', reply_markup=q3_markup, parse_mode='Markdown')
        return score
    if callback.data.startswith('quiz_q4'):
        score.append(callback.data)
        await callback.message.answer('_"Скільки вібраторів ти вже маєш?"_', reply_markup=q4_markup, parse_mode='Markdown')
        return score
    if callback.data.startswith('quiz_qend'):
        score.append(callback.data)
        if 'quiz_q25' in score:
            link = get_random_link(
                get_links('https://lovespace.ua/uk/catalog/klitoralnye'))
            await callback.message.answer('Спробуй це 😏')
            await callback.message.answer(link)
            await callback.message.answer('Або переглянь інші товари у цій категорії 👀')
            await callback.message.answer('https://lovespace.ua/uk/catalog/klitoralnye')
            return []
        if 'quiz_q24' in score:
            link = get_random_link(
                get_links('https://lovespace.ua/uk/catalog/vaginalnye'))
            await callback.message.answer('Спробуй це 😏')
            await callback.message.answer(link)
            await callback.message.answer('Або переглянь інші товари у цій категорії 👀')
            await callback.message.answer('https://lovespace.ua/uk/catalog/vaginalnye')
            return []
        if 'quiz_q22' in score:
            link = get_random_link(
                get_links('https://lovespace.ua/uk/catalog/dvojnye-vibratory'))
            await callback.message.answer('Спробуй це 😏')
            await callback.message.answer(link)
            await callback.message.answer('Або переглянь інші товари у цій категорії 👀')
            await callback.message.answer('https://lovespace.ua/uk/catalog/dvojnye-vibratory')
            return []
        if 'quiz_q21' in score:
            link = get_random_link(
                get_links('https://lovespace.ua/uk/catalog/nabori-igrashok'))
            await callback.message.answer('Спробуй це 😏')
            await callback.message.answer(link)
            await callback.message.answer('Або переглянь інші товари у цій категорії 👀')
            await callback.message.answer('https://lovespace.ua/uk/catalog/nabori-igrashok')
            return []
