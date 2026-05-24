import os
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")

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

    user = await users.find_one({"user_id": user_id})

    if not user:

        await users.insert_one({
            "user_id": user_id
        })


async def is_joined(user_id):

    try:

        member = await bot.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:
            return True

    except:
        return False

    return False


async def force_sub_message(message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "JOIN CHANNEL",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@','')}"
                )
            ],
            [
                InlineKeyboardButton(
                    "TRY AGAIN",
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


async def log_message(text):

    try:

        await bot.send_message(
            LOG_CHANNEL,
            text
        )

    except Exception as e:
        print(e)

# ================= START =================

@bot.on_message(filters.command("start"))

async def start_handler(client, message):

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:

        return await force_sub_message(message)

    await add_user(user_id)

    await log_message(
        f"""
🆕 New User Started Bot

👤 Name: {message.from_user.first_name}
🆔 ID: {user_id}
"""
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "AI CHAT",
                    callback_data="ai_chat"
                ),

                InlineKeyboardButton(
                    "SUPPORT",
                    callback_data="support"
                )
            ],

            [
                InlineKeyboardButton(
                    "HELP",
                    callback_data="help"
                )
            ]
        ]
    )

    msg = await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

Welcome To Technician AI Bot

✅ AI Chat
✅ Troubleshooting
✅ Support
✅ Smart Assistant
""",
        reply_markup=buttons
    )

    await asyncio.sleep(AUTO_DELETE_TIME)

    try:
        await msg.delete()
    except:
        pass

# ================= CALLBACKS =================

@bot.on_callback_query()

async def callbacks(client, query):

    data = query.data

    # ===== CHECK FORCE SUB =====

    if data == "checksub":

        joined = await is_joined(query.from_user.id)

        if joined:

            return await query.message.edit_text(
                "✅ Access Granted!\nSend /start"
            )

        else:

            return await query.answer(
                "Join Channel First",
                show_alert=True
            )

    # ===== AI CHAT =====

    if data == "ai_chat":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK",
                        callback_data="back_home"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            """
🤖 AI Chat Enabled

Now Send Your Issue

Example:
Samsung A13 No Charging
""",
            reply_markup=buttons
        )

    # ===== SUPPORT =====

    elif data == "support":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK",
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
                        "BACK",
                        callback_data="back_home"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            """
📚 Help Menu

Send phone issue like:

• No Charging
• Dead Phone
• No Display
• Restart
• Short Issue
""",
            reply_markup=buttons
        )

    # ===== BACK =====

    elif data == "back_home":

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "AI CHAT",
                        callback_data="ai_chat"
                    ),

                    InlineKeyboardButton(
                        "SUPPORT",
                        callback_data="support"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "HELP",
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

# ================= AI MESSAGE =================

@bot.on_message(filters.text & ~filters.command(["start"]))

async def ai_handler(client, message):

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:

        return await force_sub_message(message)

    text = message.text.lower()

    await log_message(
        f"""
💬 New Message

👤 User: {message.from_user.first_name}
🆔 ID: {user_id}

📩 Message:
{text}
"""
    )

    # ===== TROUBLESHOOTING =====

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

        msg = await message.reply_text(
            """
🔍 Step 1

6 Port Amp Edukkundo?
""",
            reply_markup=buttons
        )

        await asyncio.sleep(AUTO_DELETE_TIME)

        try:
            await msg.delete()
        except:
            pass

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

# ================= CHARGING FLOW =================

@bot.on_callback_query(filters.regex("charge_yes"))

async def charge_yes(client, query):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "OK",
                    callback_data="battery_ok"
                ),

                InlineKeyboardButton(
                    "NOT OK",
                    callback_data="battery_no"
                )
            ],

            [
                InlineKeyboardButton(
                    "BACK",
                    callback_data="back_home"
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


@bot.on_callback_query(filters.regex("charge_no"))

async def charge_no(client, query):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "DONE",
                    callback_data="cc_done"
                )
            ],

            [
                InlineKeyboardButton(
                    "BACK",
                    callback_data="back_home"
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

# ================= RUN =================

async def main():

    await bot.start()

    print("Bot Started Successfully!")

    app.run(
        host="0.0.0.0",
        port=8000
    )

asyncio.run(main())