from pyrogram import Client, idle

from config import *
from handlers.start import register_start
from handlers.support import register_support
from handlers.admin import register_admin
from utils.database import load_database

app = Client(
    "MobileSupportBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def startup():
    print("Loading Database...")
    await load_database(app)

    register_start(app)
    register_support(app)
    register_admin(app)

    print("Bot Started Successfully.")

app.start()
app.loop.run_until_complete(startup())
idle()
app.stop()
