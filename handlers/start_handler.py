from telegram import Update
from telegram.ext import ContextTypes

from keyboards.inline_keyboards import get_direction_keyboard
from services.shared_data import question_bank


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = question_bank.get_categories()

    await update.message.reply_text(
        "Привіт. Я бот для підготовки до співбесіди.\n"
        "Оберіть напрям тестування:",
        reply_markup=get_direction_keyboard(categories),
    )
