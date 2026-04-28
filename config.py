# OLD VERSION (hardcoded, security risk):
# BOT_TOKEN = "8787189527:AAH6yNh1YOJyUfQ7uZCi0VpGRxNMm0hH4sE"
# ADMIN_IDS = [746932940]
# ADMIN_IDS = [822667976]

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

ADMIN_IDS = os.environ.get("ADMIN_IDS", "")
if not ADMIN_IDS:
    raise ValueError("ADMIN_IDS environment variable not set")

ADMIN_IDS = [int(uid.strip()) for uid in ADMIN_IDS.split(",") if uid.strip().isdigit()]
