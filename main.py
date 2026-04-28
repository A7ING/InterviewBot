import logging
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# OLD VERSION magic strings like "direction:" directly)
CALLBACK_DIRECTION_PREFIX = "direction:"
CALLBACK_ANSWER_PREFIX = "answer:"
CALLBACK_ACTION_PREFIX = "action:"


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("result", result_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("questions", questions_command))
    app.add_handler(CommandHandler("add_question", add_question_parse))
    app.add_handler(CommandHandler("edit_question", edit_question_parse))
    app.add_handler(CommandHandler("delete_question", delete_question_parse))

    app.add_handler(
        CallbackQueryHandler(
            choose_direction_callback, pattern=r"^" + CALLBACK_DIRECTION_PREFIX
        )
    )
    app.add_handler(
        CallbackQueryHandler(answer_callback, pattern=r"^" + CALLBACK_ANSWER_PREFIX)
    )
    app.add_handler(
        CallbackQueryHandler(action_callback, pattern=r"^" + CALLBACK_ACTION_PREFIX)
    )

    # OLD VERSION (no error handling):
    # print("Bot is running...")
    # app.run_polling()

    print("Bot is running...")
    try:
        app.run_polling()
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}", exc_info=True)
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()
