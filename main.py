from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers.start_handler import start_command
from handlers.test_handler import (
    choose_direction_callback,
    answer_callback,
    result_command,
    action_callback,
)
from handlers.admin_handler import (
    admin_command,
    questions_command,
    add_question_parse,
    edit_question_parse,
    delete_question_parse,
)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("result", result_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("questions", questions_command))
    app.add_handler(CommandHandler("add_question", add_question_parse))
    app.add_handler(CommandHandler("edit_question", edit_question_parse))
    app.add_handler(CommandHandler("delete_question", delete_question_parse))

    app.add_handler(CallbackQueryHandler(choose_direction_callback, pattern=r"^direction:"))
    app.add_handler(CallbackQueryHandler(answer_callback, pattern=r"^answer:"))
    app.add_handler(CallbackQueryHandler(action_callback, pattern=r"^action:"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()