from pyrogram import Client, idle
from flask import Flask
from threading import Thread
import os
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
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot Running"

def run_web():
    port = int(os.environ.get("PORT", 8000))
    web.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

app.start()
app.loop.run_until_complete(startup())
idle()
app.stop()
