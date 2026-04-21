from telegram import Update
from telegram.ext import ContextTypes
import html

from keyboards.inline_keyboards import (
    get_direction_keyboard,
    get_post_test_keyboard,
    get_question_keyboard,
)
from services.shared_data import question_bank, session_service, history_service


async def choose_direction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    direction = query.data.split(":", 1)[1]
    user_id = query.from_user.id

    questions = question_bank.get_questions_by_category(direction)

    if not questions:
        await query.edit_message_text("Для цього напряму питань поки немає.")
        return

    session = session_service.create_session(user_id, direction, questions)
    question = session.get_current_question()

    safe_question_text = html.escape(question.text)

    text = f"Напрям: {direction}\nПочинаємо тест.\n\n<b>{safe_question_text}</b>\n\n"
    for i, option in enumerate(question.options, 1):
        safe_option = html.escape(option)
        text += f"{i}) {safe_option}\n"

    await query.edit_message_text(
        text=text, reply_markup=get_question_keyboard(question), parse_mode="HTML"
    )


async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = session_service.get_session(user_id)

    if session is None:
        await query.edit_message_text("Сесію не знайдено. Натисніть /start")
        return

    option_index = int(query.data.split(":", 1)[1])
    session.submit_answer(option_index)

    next_question = session.get_current_question()

    if next_question is not None:
        safe_question_text = html.escape(next_question.text)

        text = f"<b>{safe_question_text}</b>\n\n"
        for i, option in enumerate(next_question.options, 1):
            safe_option = html.escape(option)
            text += f"{i}) {safe_option}\n"

        await query.edit_message_text(
            text=text,
            reply_markup=get_question_keyboard(next_question),
            parse_mode="HTML",
        )
    else:
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


async def result_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(history_service.format_user_history(user_id))


async def action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    action = query.data.split(":", 1)[1]

    if action == "restart":
        categories = question_bank.get_categories()
        await query.edit_message_text(
            text="Оберіть напрям для нового тесту:",
            reply_markup=get_direction_keyboard(categories),
        )

    elif action == "stats":
        await query.edit_message_text(text=history_service.format_user_history(user_id))
