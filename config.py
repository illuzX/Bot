import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

FORCE_SUB_CHANNEL = int(
    os.getenv("FORCE_SUB_CHANNEL")
)

FORCE_SUB_LINK = os.getenv(
    "FORCE_SUB_LINK"
)

LOG_CHANNEL = int(
    os.getenv("LOG_CHANNEL")
)

ADMINS = [681308121]
