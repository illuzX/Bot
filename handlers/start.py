from pyrogram import Client, filters
from pyrogram.types import Message

from database.mongo import add_user, is_banned


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client, message: Message):

    user_id = message.from_user.id

    if await is_banned(user_id):
        return await message.reply_text(
            "🚫 You are banned from using this bot."
        )

    await add_user(
        user_id,
        message.from_user.first_name
    )

    await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

✅ Bot Working Successfully
✅ MongoDB Connected
✅ Advanced System Enabled
"""
    )