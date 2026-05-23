from flask import Flask
from threading import Thread
import os

from pyrogram import Client, idle

from config import *

from handlers.start import register_start
from handlers.support import register_support
from handlers.admin import register_admin
from handlers.callbacks import register_callbacks
from handlers.inline import register_inline

# ---------------- WEB ---------------- #

web = Flask(__name__)

@web.route("/")
def home():
    return "Advanced GSM Bot Running"

def run_web():

    port = int(
        os.environ.get("PORT", 8000)
    )

    web.run(
        host="0.0.0.0",
        port=port
    )

Thread(target=run_web).start()

# ---------------- BOT ---------------- #

app = Client(
    "AdvancedGSMSupportBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_start(app)
register_support(app)
register_admin(app)
register_callbacks(app)
register_inline(app)

app.start()

print("BOT STARTED")

idle()

app.stop()
