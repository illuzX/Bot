import os
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
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL").replace("@", "")

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

def run_web():
    app.run(
        host="0.0.0.0",
        port=8000
    )

# ================= FORCE SUB =================

async def is_joined(user_id):

    try:

        member = await bot.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        return member.status not in ["kicked", "left"]

    except UserNotParticipant:
        return False

    except Exception as e:
        print("ForceSub Error:", e)
        return True


async def force_sub(message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "JOIN CHANNEL",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL}"
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

    await message.reply_text(
        "⚠️ Please Join Our Channel First",
        reply_markup=buttons
    )

# ================= START =================

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:
        return await force_sub(message)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "AI CHAT",
                    callback_data="ai"
                )
            ]
        ]
    )

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}",
        reply_markup=buttons
    )

# ================= CALLBACK =================

@bot.on_callback_query()
async def callback_handler(client, query):

    if query.data == "checksub":

        joined = await is_joined(query.from_user.id)

        if joined:

            await query.message.edit_text(
                "✅ Access Granted\nSend /start"
            )

        else:

            await query.answer(
                "Join Channel First",
                show_alert=True
            )

    elif query.data == "ai":

        await query.message.edit_text(
            "🤖 Send Your Problem"
        )

# ================= AI =================

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def ai_handler(client, message):

    if not message.from_user:
        return

    user_id = message.from_user.id

    joined = await is_joined(user_id)

    if not joined:
        return await force_sub(message)

    text = message.text.lower()

    print(text)

    if "charging" in text:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "YES",
                        callback_data="yes"
                    ),

                    InlineKeyboardButton(
                        "NO",
                        callback_data="no"
                    )
                ]
            ]
        )

        await message.reply_text(
            "6 Port Amp Edukkundo?",
            reply_markup=buttons
        )

    else:

        await message.reply_text(
            "🤖 AI Processing..."
        )

# ================= RUN =================

if __name__ == "__main__":

    threading.Thread(
        target=run_web
    ).start()

    print("Bot Started Successfully!")

    bot.run()
