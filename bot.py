import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from motor.motor_asyncio import AsyncIOMotorClient
from threading import Thread

# =========================
# EVENT LOOP FIX
# =========================

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# =========================
# CONFIG
# =========================

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# =========================
# FLASK SERVER (Koyeb Keep Alive)
# =========================

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot Is Running Successfully!"

def run_web():
    web_app.run(host="0.0.0.0", port=8000)

# =========================
# TELEGRAM BOT
# =========================

bot = Client(
    "AdvancedBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# MONGODB
# =========================

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["telegram_bot"]

users = db["users"]
banned = db["banned"]

# =========================
# DATABASE FUNCTIONS
# =========================

async def add_user(user_id):
    user = await users.find_one({"user_id": user_id})

    if not user:
        await users.insert_one({
            "user_id": user_id
        })

async def is_banned(user_id):
    user = await banned.find_one({
        "user_id": user_id
    })

    return bool(user)

async def ban_user(user_id):
    already = await banned.find_one({
        "user_id": user_id
    })

    if not already:
        await banned.insert_one({
            "user_id": user_id
        })

async def unban_user(user_id):
    await banned.delete_one({
        "user_id": user_id
    })

# =========================
# START COMMAND
# =========================

@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):

    user_id = message.from_user.id

    await add_user(user_id)

    if await is_banned(user_id):
        return await message.reply_text(
            "❌ You Are Banned!"
        )

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}\n\n"
        f"✅ Advanced Bot Running Successfully!"
    )

# =========================
# PING
# =========================

@bot.on_message(filters.command("ping"))
async def ping_handler(client, message: Message):

    await message.reply_text("🏓 Pong!")

# =========================
# STATS
# =========================

@bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client, message: Message):

    total_users = await users.count_documents({})
    total_banned = await banned.count_documents({})

    text = (
        f"📊 Bot Statistics\n\n"
        f"👥 Users: {total_users}\n"
        f"🚫 Banned: {total_banned}"
    )

    await message.reply_text(text)

# =========================
# BROADCAST
# =========================

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/broadcast Hello"
        )

    broadcast_msg = message.text.split(None, 1)[1]

    success = 0
    failed = 0

    async for user in users.find():

        try:
            await bot.send_message(
                user["user_id"],
                broadcast_msg
            )

            success += 1

        except:
            failed += 1

    await message.reply_text(
        f"✅ Broadcast Completed\n\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

# =========================
# BAN USER
# =========================

@bot.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_handler(client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/ban user_id"
        )

    user_id = int(message.command[1])

    await ban_user(user_id)

    await message.reply_text(
        f"🚫 User {user_id} banned."
    )

# =========================
# UNBAN USER
# =========================

@bot.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_handler(client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/unban user_id"
        )

    user_id = int(message.command[1])

    await unban_user(user_id)

    await message.reply_text(
        f"✅ User {user_id} unbanned."
    )

# =========================
# SUPPORT SYSTEM
# =========================

@bot.on_message(filters.private & ~filters.command([
    "start",
    "ping",
    "stats",
    "broadcast",
    "ban",
    "unban"
]))
async def support_handler(client, message: Message):

    user_id = message.from_user.id

    if user_id == OWNER_ID:
        return

    if await is_banned(user_id):
        return

    text = (
        f"📩 New Support Message\n\n"
        f"👤 User: {message.from_user.mention}\n"
        f"🆔 ID: `{user_id}`\n\n"
        f"💬 Message:\n{message.text}"
    )

    await bot.send_message(
        OWNER_ID,
        text
    )

    await message.reply_text(
        "✅ Your message sent to admin."
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    Thread(target=run_web).start()

    print("Bot Started Successfully!")

    bot.run()
