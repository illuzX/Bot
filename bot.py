import os
import asyncio
import threading

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
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

# username matram
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL").replace("@", "")

AUTO_DELETE_TIME = 30

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
    return "Bot Running Successfully!"

# ================= HELPERS =================

async def add_user(user_id):

    user = await users.find_one({
        "user_id": user_id
    })

    if not user:

        await users.insert_one({
            "user_id": user_id
        })


# ===== FORCE SUB CHECK =====

async def is_joined(user_id):

    try:

        member = await bot.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        print(member.status)

        # LEFT / BANNED mathram reject cheyyu
        if str(member.status) in [
            "ChatMemberStatus.BANNED",
            "ChatMemberStatus.LEFT",
            "banned",
            "left"
        ]:
            return False

        return True

    except UserNotParticipant:
        return False

    except Exception as e:
        print(f"ForceSub Error: {e}")
        return True


# ===== FORCE SUB MESSAGE =====

async def force_sub_message(message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 JOIN CHANNEL",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ TRY AGAIN",
                    callback_data="checksub"
                )
            ]
        ]
    )

    return await message.reply_text(
        "⚠️ Please Join Our Updates Channel First!",
        reply_markup=buttons
    )


# ===== LOGS =====

async def log_message(text):

    try:

        await bot.send_message(
            LOG_CHANNEL,
            text
        )

    except Exception as e:
        print(f"Log Error: {e}")

# ================= START =================

@bot.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:
        return await force_sub_message(message)

    await add_user(user_id)

    await log_message(
        f"""
🆕 New User

👤 {message.from_user.first_name}
🆔 {user_id}
"""
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🤖 AI CHAT",
                    callback_data="ai_chat"
                ),

                InlineKeyboardButton(
                    "📚 HELP",
                    callback_data="help"
                )
            ],

            [
                InlineKeyboardButton(
                    "🛠 SUPPORT",
                    callback_data="support"
                )
            ]
        ]
    )

    await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

Welcome To Technician AI Bot
""",
        reply_markup=buttons
    )

# ================= CALLBACKS =================

@bot.on_callback_query()
async def callbacks(client, query):

    data = query.data

    # ===== CHECK SUB =====

    if data == "checksub":

        joined = await is_joined(query.from_user.id)

        if joined:

            return await query.message.edit_text(
                "✅ Access Granted!\n\nSend /start"
            )

        else:

            return await query.answer(
                "❌ Join Channel First",
                show_alert=True
            )

    # ===== AI CHAT =====

    elif data == "ai_chat":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅️ BACK",
                        callback_data="back_home"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            """
🤖 Send Your Issue

Example:
Samsung A13 No Charging
""",
            reply_markup=buttons
        )

    # ===== HELP =====

    elif data == "help":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅️ BACK",
                        callback_data="back_home"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            """
📚 Supported Issues

• Charging
• Dead
• Restart
• No Display
• Short
""",
            reply_markup=buttons
        )

    # ===== SUPPORT =====

    elif data == "support":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅️ BACK",
                        callback_data="back_home"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            """
🛠 Support

Contact Admin:
@yourusername
""",
            reply_markup=buttons
        )

    # ===== BACK =====

    elif data == "back_home":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🤖 AI CHAT",
                        callback_data="ai_chat"
                    ),

                    InlineKeyboardButton(
                        "📚 HELP",
                        callback_data="help"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🛠 SUPPORT",
                        callback_data="support"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            "🏠 Home Menu",
            reply_markup=buttons
        )

    # ===== CHARGING FLOW =====

    elif data == "charge_yes":

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

Check CC Line Voltage
"""
        )

# ================= AI =================

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def ai_handler(client, message):

    try:

        if not message.from_user:
            return

        user_id = message.from_user.id

        joined = await is_joined(user_id)

        if not joined:
            return await force_sub_message(message)

        text = message.text.lower()

        await log_message(
            f"""
💬 New Message

👤 {message.from_user.first_name}
🆔 {user_id}

📩 {text}
"""
        )

        # ===== CHARGING =====

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

            await message.reply_text(
                """
🔍 Step 1

6 Port Amp Edukkundo?
""",
                reply_markup=buttons
            )

        else:

            await message.reply_text(
                """
🤖 AI Learning Mode

Try Detailed Issue
"""
            )

    except Exception as e:
        print(f"AI ERROR: {e}")

# ================= RUN =================

def run_flask():

    app.run(
        host="0.0.0.0",
        port=8000
    )

async def main():

    threading.Thread(
        target=run_flask
    ).start()

    await bot.start()

    print("Bot Started Successfully!")

    await asyncio.Event().wait()

if __name__ == "__main__":

    asyncio.run(main())
