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
review = KeyboardButton("Відкрий скарбничку з іграшками 🧸")
subscribe = KeyboardButton("Підписатись на щоденний контент 🔔")
need_help = KeyboardButton("Допомога ℹ️")

main_menu = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[[talk], [quiz, story], [
        kamasutra, review], [subscribe], [need_help]],
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

orientation_keyboard = InlineKeyboardMarkup(row_width=1)
orientation_keyboard.add(
    InlineKeyboardButton(text="Гетеросексуал", callback_data="hetero"),
    InlineKeyboardButton(text="Гомосексуал", callback_data="homo"),
    InlineKeyboardButton(text="Бісексуал", callback_data="bi")
)


vibrator_quiz = InlineKeyboardButton(
    text="Який вібратор тобі підходить 💦", callback_data='vibrator_quiz')


def create_question_btn(answers: list, next_question: str):
    btns = []
    for answer in answers:
        btns.append(InlineKeyboardButton(
            text=answer[0], callback_data=f'quiz_q{next_question}{answer[1]}'))
    return btns


question_1 = [("Cтимуляція клітора", 5), ("Вагінальне проникнення", 4),
              ("Не можу обрати між першим і другим", 2), ("Не знаю, але хочу дізнатися", 1)]
question_2 = [("Широка та гучна вібрація", 5), ("Інтенсивна, цілеспрямована стимуляція", 4),
              ("Ніжний дотик", 2), ("Все, що схоже на оральний секс", 1)]
question_3 = [("10 хвилин ⏱️", 2), ("Досить для солідної сесії 😊", 4),
              ("Весь день, крихітко 😎", 5)]
question_4 = [("Жодного, це мій перший раз 🙄", 1), ("Два чи три 🤫", 4),
              ("Називай мене колекціонером 🤭", 5)]

vibrator_q1 = create_question_btn(question_1, '2')
vibrator_q2 = create_question_btn(question_2, '3')
vibrator_q3 = create_question_btn(question_3, '4')
vibrator_q4 = create_question_btn(question_4, 'end')

main_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_admin.add('Поза дня').add('Секс-історія').add('Секс-шоп').add('Додати ревью на товар')

adminpanel = InlineKeyboardMarkup(row_width=1)
adminpanel.add(
    InlineKeyboardButton(text="Додати контент", callback_data="add"),
    InlineKeyboardButton(text="Видалити контент", callback_data="delete"),
    InlineKeyboardButton(text="Зробити розсилку", callback_data="mail"),
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add("Назад")


read_story = InlineKeyboardButton(
    'Читати історію 🗞️', callback_data='read_story')
add_story = InlineKeyboardButton(
    'Розказати свою 🖋️', callback_data='add_story')

story_markup = InlineKeyboardMarkup(row_width=2).add(read_story, add_story)
