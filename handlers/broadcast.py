from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMINS
from database.mongo import get_users


@Client.on_message(filters.command("broadcast"))
async def broadcast_handler(client, message: Message):

    if message.from_user.id not in ADMINS:
        return

    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To Message"
        )

    users = await get_users()

    success = 0
    failed = 0

    for user in users:

        try:
            await message.reply_to_message.copy(user)
            success += 1

        except:
            failed += 1

    await message.reply_text(
        f"""
✅ Broadcast Completed

Success: {success}
Failed: {failed}
"""
    )