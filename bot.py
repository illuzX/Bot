import os
import asyncio
from threading import Thread

from flask import Flask

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pyrogram.errors import UserNotParticipant

from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv

# ================= LOAD ENV =================

load_dotenv()

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))

API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

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

    try:

        user = await users.find_one(
            {"user_id": user_id}
        )

        if not user:

            await users.insert_one(
                {
                    "user_id": user_id
                }
            )

    except Exception as e:

        print(f"Add User Error: {e}")

# ================= LOGS =================

async def log_message(text):

    try:

        await bot.send_message(
            LOG_CHANNEL,
            text
        )

    except Exception as e:

        print(f"Log Error: {e}")

# ================= FORCE SUB =================

async def is_joined(user_id):

    try:

        member = await bot.get_chat_member(
            chat_id=f"@{FORCE_SUB_CHANNEL}",
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:
            return True

        return False

    except UserNotParticipant:

        return False

    except Exception as e:

        print(f"ForceSub Error: {e}")

        return False


async def force_sub_message(message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Try Again",
                    callback_data="checksub"
                )
            ]
        ]
    )

    msg = await message.reply_text(
        "⚠️ Please Join Our Channel First!",
        reply_markup=buttons
    )

    await asyncio.sleep(AUTO_DELETE_TIME)

    try:
        await msg.delete()
    except:
        pass

# ================= START =================

@bot.on_message(
    filters.private &
    filters.command("start")
)
async def start_handler(client, message):

    try:

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

👤 Name: {message.from_user.first_name}

🆔 ID: {user_id}
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
                        "🛠 SUPPORT",
                        callback_data="support"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "📚 HELP",
                        callback_data="help"
                    )
                ]
            ]
        )

        msg = await message.reply_text(
            f"""
👋 Hello {message.from_user.first_name}

Welcome To Technician AI Bot

✅ AI Troubleshooting
✅ Charging Diagnosis
✅ Support System
✅ Smart Assistant
""",
            reply_markup=buttons
        )

        await asyncio.sleep(AUTO_DELETE_TIME)

        try:
            await msg.delete()
        except:
            pass

    except Exception as e:

        print(f"Start Error: {e}")

# ================= CALLBACKS =================

@bot.on_callback_query()
async def callbacks(client, query):

    try:

        data = query.data

        # ===== CHECK SUB =====

        if data == "checksub":

            joined = await is_joined(
                query.from_user.id
            )

            if joined:

                return await query.message.edit_text(
                    "✅ Subscription Verified!\n\nSend /start"
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
                            "🔙 BACK",
                            callback_data="back_home"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
🤖 AI Chat Enabled

Send Problem Like:

• Samsung A13 No Charging
• Dead Phone
• Restart Issue
• No Display
""",
                reply_markup=buttons
            )

        # ===== SUPPORT =====

        elif data == "support":

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 BACK",
                            callback_data="back_home"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
🛠 Support Section

Contact Admin:
@yourusername
""",
                reply_markup=buttons
            )

        # ===== HELP =====

        elif data == "help":

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 BACK",
                            callback_data="back_home"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
📚 Help Menu

Send Issues Like:

• No Charging
• Dead
• Short
• Restart
• No Boot
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
                            "🛠 SUPPORT",
                            callback_data="support"
                        )
                    ],

                    [
                        InlineKeyboardButton(
                            "📚 HELP",
                            callback_data="help"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
🏠 Home Menu
""",
                reply_markup=buttons
            )

        # ===== CHARGING FLOW =====

        elif data == "charge_yes":

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ OK",
                            callback_data="battery_ok"
                        ),

                        InlineKeyboardButton(
                            "❌ NOT OK",
                            callback_data="battery_no"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
🔍 Step 2

Battery Percentage Increasing Undo?
""",
                reply_markup=buttons
            )

        elif data == "charge_no":

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ DONE",
                            callback_data="cc_done"
                        )
                    ]
                ]
            )

            await query.message.edit_text(
                """
🔍 Step 2

Check CC Line Voltage
""",
                reply_markup=buttons
            )

    except Exception as e:

        print(f"Callback Error: {e}")

# ================= AI HANDLER =================

@bot.on_message(
    filters.private &
    filters.text &
    ~filters.command(["start"])
)
async def ai_handler(client, message):

    try:

        if not message.from_user:
            return

        user_id = message.from_user.id

        joined = await is_joined(user_id)

        if not joined:

            return await force_sub_message(message)

        text = (message.text or "").lower()

        await log_message(
            f"""
💬 New Message

👤 User: {message.from_user.first_name}

🆔 ID: {user_id}

📩 Message:
{text}
"""
        )

        # ===== CHARGING ISSUE =====

        if "charging" in text:

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ YES",
                            callback_data="charge_yes"
                        ),

                        InlineKeyboardButton(
                            "❌ NO",
                            callback_data="charge_no"
                        )
                    ]
                ]
            )

            msg = await message.reply_text(
                """
🔍 Step 1

6 Port Amp Edukkundo?
""",
                reply_markup=buttons
            )

        else:

            msg = await message.reply_text(
                """
🤖 AI Reply

Currently Learning This Issue...
"""
            )

        await asyncio.sleep(AUTO_DELETE_TIME)

        try:
            await msg.delete()
        except:
            pass

    except Exception as e:

        print(f"AI Handler Error: {e}")

# ================= WEB SERVER =================

def run_web():

    app.run(
        host="0.0.0.0",
        port=8000
    )

# ================= START =================

if __name__ == "__main__":

    web_thread = Thread(
        target=run_web
    )

    web_thread.start()

    print("Bot Started Successfully!")

    bot.run()
