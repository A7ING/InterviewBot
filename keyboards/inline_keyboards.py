from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_direction_keyboard(categories):
    keyboard = []
    for category in categories:
        keyboard.append(
            [InlineKeyboardButton(category, callback_data=f"direction:{category}")]
        )
    return InlineKeyboardMarkup(keyboard)


def get_question_keyboard(question):
    keyboard = []
    row = []

    for index, _ in enumerate(question.options):
        row.append(
            InlineKeyboardButton(str(index + 1), callback_data=f"answer:{index}")
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_post_test_keyboard():
    keyboard = [
        [InlineKeyboardButton("Пройти тест ще раз", callback_data="action:restart")],
        [InlineKeyboardButton("Статистика за весь час", callback_data="action:stats")],
    ]
    return InlineKeyboardMarkup(keyboard)
