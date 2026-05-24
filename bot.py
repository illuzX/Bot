import os
import asyncio
import threading

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

FORCE_SUB_CHANNEL = os.getenv(
    "FORCE_SUB_CHANNEL"
).replace("@", "")

# ================= DATABASE =================

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["techbot"]

users = db["users"]

# ================= BOT =================

bot = Client(
    "TechBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running!"

# ================= FORCE SUB =================

async def is_joined(user_id):

    try:

        member = await bot.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        banned_status = [
            "ChatMemberStatus.LEFT",
            "ChatMemberStatus.BANNED",
            "left",
            "kicked",
            "banned"
        ]

        if str(member.status) in banned_status:
            return False

        return True

    except UserNotParticipant:
        return False

    except Exception as e:

        print(f"ForceSub Error: {e}")

        return True

# ================= START =================

@bot.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 JOIN CHANNEL",
                        url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                    )
                ]
            ]
        )

        return await message.reply_text(
            "⚠️ Join Channel First",
            reply_markup=buttons
        )

    await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

✅ Bot Working Properly
"""
    )

# ================= AI =================

@bot.on_message(
    filters.private &
    filters.text &
    ~filters.command(["start"])
)
async def ai_handler(client, message):

    if not message.from_user:
        return

    text = message.text.lower()

    if "charging" in text:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "YES",
                        callback_data="charge_yes"
                    ),

                    InlineKeyboardButton(
                        "NO",
                        callback_data="charge_no"
                    )
                ]
            ]
        )

        return await message.reply_text(
            """
🔍 Step 1

6 Port Amp Edukkundo?
""",
            reply_markup=buttons
        )

    else:

        return await message.reply_text(
            "🤖 AI Learning..."
        )

# ================= CALLBACK =================

@bot.on_callback_query()
async def callback_handler(client, query):

    data = query.data

    if data == "charge_yes":

        await query.message.edit_text(
            """
🔍 Step 2

Battery Percentage Increasing Undo?
"""
        )

    elif data == "charge_no":

        await query.message.edit_text(
            """
🔍 Step 2

Check CC Line
"""
        )

# ================= FLASK THREAD =================

def run_flask():

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False
    )

# ================= MAIN =================

async def main():

    threading.Thread(
        target=run_flask
    ).start()

    print("Starting Bot...")

    await bot.start()

    print("Bot Started Successfully!")

    await idle()

from pyrogram.idle import idle

if __name__ == "__main__":

    asyncio.run(main())
