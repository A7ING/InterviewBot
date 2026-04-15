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
    for index, option in enumerate(question.options):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"answer:{index}")]
        )
    return InlineKeyboardMarkup(keyboard)


def get_post_test_keyboard():
    keyboard = [
        [InlineKeyboardButton("Пройти тест ще раз", callback_data="action:restart")],
        [InlineKeyboardButton("Статистика за весь час", callback_data="action:stats")],
    ]
    return InlineKeyboardMarkup(keyboard)