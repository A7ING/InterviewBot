import asyncio
import os
import sys
import types
from types import SimpleNamespace
from unittest.mock import AsyncMock

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token")
os.environ.setdefault("ADMIN_IDS", "1,2")

telegram_module = types.ModuleType("telegram")
telegram_module.Update = object
sys.modules["telegram"] = telegram_module

telegram_ext_module = types.ModuleType("telegram.ext")
telegram_ext_module.ContextTypes = SimpleNamespace(DEFAULT_TYPE=object)
sys.modules["telegram.ext"] = telegram_ext_module

from handlers.admin_handler import (  # noqa: E402
    is_admin,
    safe_int as admin_safe_int,
    delete_question_parse,
)
from handlers.test_handler import safe_int as handler_safe_int  # noqa: E402


class DummyMessage:
    def __init__(self, text=""):
        self.text = text
        self.reply_text = AsyncMock()


class DummyUser:
    def __init__(self, user_id):
        self.id = user_id


class DummyUpdate:
    def __init__(self, user_id, text=""):
        self.effective_user = DummyUser(user_id)
        self.message = DummyMessage(text)


def test_admin_safe_int_returns_number_for_valid_input():
    assert admin_safe_int("15") == 15


def test_admin_safe_int_returns_default_for_invalid_input():
    assert admin_safe_int("abc", -1) == -1
    assert admin_safe_int(None, -1) == -1


def test_handler_safe_int_returns_default_for_invalid_input():
    assert handler_safe_int("xyz", -1) == -1


def test_is_admin_returns_true_for_allowed_user():
    assert is_admin(1) is True


def test_is_admin_returns_false_for_unknown_user():
    assert is_admin(999) is False


def test_delete_question_parse_rejects_invalid_id():
    update = DummyUpdate(user_id=1, text="/delete_question abc")
    context = SimpleNamespace()

    asyncio.run(delete_question_parse(update, context))

    update.message.reply_text.assert_awaited_once_with("Невірний формат ID.")


def test_delete_question_parse_rejects_non_admin():
    update = DummyUpdate(user_id=999, text="/delete_question 1")
    context = SimpleNamespace()

    asyncio.run(delete_question_parse(update, context))

    update.message.reply_text.assert_awaited_once_with("У вас немає доступу.")
