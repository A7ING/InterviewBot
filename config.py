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
