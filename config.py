from os import getenv
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_USER = quote_plus(getenv("MONGO_USER"))
MONGO_PASS = quote_plus(getenv("MONGO_PASS"))

MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}"
    "@cluster0.djvuojm.mongodb.net/"
    "telegram_bot"
    "?retryWrites=true&w=majority&appName=Cluster0"
)

ADMINS = list(map(int, getenv("ADMINS").split()))
