from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMINS
from database.mongo import (
    total_users,
    ban_user,
    unban_user
)


@Client.on_message(filters.command("stats"))
async def stats_handler(client, message: Message):

    if message.from_user.id not in ADMINS:
        return

    users = await total_users()

    await message.reply_text(
        f"📊 Total Users: {users}"
    )


@Client.on_message(filters.command("ban"))
async def ban_handler(client, message: Message):

    if message.from_user.id not in ADMINS:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "/ban user_id"
        )

    user_id = int(message.command[1])

    await ban_user(user_id)

    await message.reply_text(
        "✅ User Banned"
    )


@Client.on_message(filters.command("unban"))
async def unban_handler(client, message: Message):

    if message.from_user.id not in ADMINS:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "/unban user_id"
        )

    user_id = int(message.command[1])

    await unban_user(user_id)

    await message.reply_text(
        "✅ User Unbanned"
    )