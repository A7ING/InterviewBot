from typing import Any
import html

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes

from keyboards.inline_keyboards import (
    get_direction_keyboard,
    get_post_test_keyboard,
    get_question_keyboard,
)
from services.shared_data import question_bank, session_service, history_service


CALLBACK_DIRECTION_PREFIX = "direction:"
CALLBACK_ANSWER_PREFIX = "answer:"
CALLBACK_ACTION_PREFIX = "action:"
ACTION_RESTART = "restart"
ACTION_STATS = "stats"


def safe_int(value: str, default: int = -1) -> int:
    """
    Безпечно перетворює рядок на ціле число.
    Якщо перетворення неможливе, повертає значення за замовчуванням.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def _get_callback_payload(data: str) -> str:
    """
    Витягує корисне навантаження з callback_data.
    Наприклад, з рядка 'direction:python' поверне 'python'.
    """
    return data.split(":", 1)[1]


def _format_question_message(question: Any, prefix_text: str = "") -> str:
    """
    Форматує текст питання та варіанти відповідей з HTML-екрануванням.
    Запобігає помилкам розмітки Telegram при виведенні спецсимволів
    (наприклад, < або > у коді).
    """
    safe_question_text = html.escape(question.text)

    msg_body = f"{prefix_text}<b>{safe_question_text}</b>\n\n"
    for i, option in enumerate(question.options, 1):
        safe_option = html.escape(option)
        msg_body += f"{i}) {safe_option}\n"

    return msg_body


async def _finish_test_and_show_results(
    query: CallbackQuery, session: Any, user_id: int
) -> None:
    """
    Завершує тестування: зберігає результати в базу даних,
    видаляє активну сесію та виводить фінальну статистику користувачу.
    """
    username = query.from_user.username or query.from_user.first_name
    history_service.save_test_result(
        user_id, username, session.direction, session.result
    )

    await query.edit_message_text(
        text=session.result.show_detailed_result(),
        reply_markup=get_post_test_keyboard(),
        parse_mode="HTML",
    )
    session_service.remove_session(user_id)


async def choose_direction_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обробляє натискання на кнопку вибору напрямку тестування.
    Створює нову сесію для користувача та надсилає перше питання.
    """
    query = update.callback_query
    await query.answer()

    direction = _get_callback_payload(query.data)
    user_id = query.from_user.id

    questions = question_bank.get_questions_by_category(direction)

    if not questions:
        await query.edit_message_text("Для цього напряму питань поки немає.")
        return

    session = session_service.create_session(user_id, direction, questions)
    question = session.get_current_question()

    prefix = f"Напрям: {direction}\nПочинаємо тест.\n\n"
    formatted_message = _format_question_message(question, prefix_text=prefix)

    await query.edit_message_text(
        text=formatted_message,
        reply_markup=get_question_keyboard(question),
        parse_mode="HTML",
    )


async def answer_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обробляє відповідь користувача на поточне питання.
    Перевіряє правильність, оновлює статистику сесії та видає
    наступне питання або підсумки.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = session_service.get_session(user_id)

    if session is None:
        await query.edit_message_text("Сесію не знайдено. Натисніть /start")
        return

    option_index = safe_int(_get_callback_payload(query.data), -1)
    if option_index < 0:
        await query.edit_message_text("Невірний формат відповіді.")
        return

    session.submit_answer(option_index)
    next_question = session.get_current_question()

    if next_question is not None:
        formatted_message = _format_question_message(next_question)

        await query.edit_message_text(
            text=formatted_message,
            reply_markup=get_question_keyboard(next_question),
            parse_mode="HTML",
        )
    else:
        await _finish_test_and_show_results(query, session, user_id)


async def result_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обробляє текстову команду перегляду статистики.
    Виводить користувачу історію всіх його проходжень тестів.
    """
    user_id = update.message.from_user.id
    await update.message.reply_text(history_service.format_user_history(user_id))


async def action_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обробляє кнопки дій після завершення тесту.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    action = _get_callback_payload(query.data)

    if action == ACTION_RESTART:
        categories = question_bank.get_categories()
        await query.edit_message_text(
            text="Оберіть напрям для нового тесту:",
            reply_markup=get_direction_keyboard(categories),
        )

    elif action == ACTION_STATS:
        await query.edit_message_text(text=history_service.format_user_history(user_id))
