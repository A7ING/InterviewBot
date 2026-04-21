from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS
from services.shared_data import question_bank


def is_admin(user_id):
    return user_id in ADMIN_IDS


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу до адмін-панелі.")
        return

    await update.message.reply_text(
        "Адмін-команди:\n\n"
        "/questions - список питань\n"
        "/add_question - додати питання\n"
        "/edit_question - редагувати питання\n"
        "/delete_question - видалити питання"
    )


async def questions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    await update.message.reply_text(question_bank.format_questions_list())


async def add_question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    text = (
        "Приклад формату:\n"
        "/add_question | Python | Що таке список у Python? | "
        "Тип даних,Функція,Цикл,Оператор | 0\n\n"
        "Останнє число — індекс правильної відповіді."
    )
    await update.message.reply_text(text)


async def add_question_parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    raw_text = update.message.text.replace("/add_question", "", 1).strip()

    if not raw_text:
        await add_question_command(update, context)
        return

    parts = [part.strip() for part in raw_text.split("|")]

    if len(parts) != 4:
        await update.message.reply_text("Неправильний формат команди.")
        return

    category = parts[0]
    question_text = parts[1]
    options = [option.strip() for option in parts[2].split(",")]
    correct_option = int(parts[3])

    if len(options) < 2:
        await update.message.reply_text("Має бути хоча б 2 варіанти відповіді.")
        return

    if correct_option < 0 or correct_option >= len(options):
        await update.message.reply_text("Невірний індекс правильної відповіді.")
        return

    question = question_bank.add_question(
        text=question_text,
        category=category,
        options=options,
        correct_option=correct_option,
    )

    await update.message.reply_text(
        f"Питання додано.\nID: {question.question_id}\nТекст: {question.text}"
    )


async def edit_question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    text = (
        "Приклад формату:\n"
        "/edit_question | 1 | Новий текст питання | "
        "Варіант 1,Варіант 2,Варіант 3,Варіант 4 | 2 | Python"
    )
    await update.message.reply_text(text)


async def edit_question_parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    raw_text = update.message.text.replace("/edit_question", "", 1).strip()

    if not raw_text:
        await edit_question_command(update, context)
        return

    parts = [part.strip() for part in raw_text.split("|")]

    if len(parts) != 5:
        await update.message.reply_text("Неправильний формат команди.")
        return

    question_id = int(parts[0])
    new_text = parts[1]
    new_options = [option.strip() for option in parts[2].split(",")]
    new_correct_option = int(parts[3])
    new_category = parts[4]

    if new_correct_option < 0 or new_correct_option >= len(new_options):
        await update.message.reply_text("Невірний індекс правильної відповіді.")
        return

    success = question_bank.edit_question(
        question_id=question_id,
        new_text=new_text,
        new_category=new_category,
        new_options=new_options,
        new_correct_option=new_correct_option,
    )

    if success:
        await update.message.reply_text("Питання успішно оновлено.")
    else:
        await update.message.reply_text("Питання з таким ID не знайдено.")


async def delete_question_parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("У вас немає доступу.")
        return

    raw_text = update.message.text.replace("/delete_question", "", 1).strip()

    if not raw_text:
        await update.message.reply_text("Приклад: /delete_question 1")
        return

    question_id = int(raw_text)
    success = question_bank.delete_question(question_id)

    if success:
        await update.message.reply_text("Питання видалено.")
    else:
        await update.message.reply_text("Питання з таким ID не знайдено.")
