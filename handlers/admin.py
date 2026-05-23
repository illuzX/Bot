from pyrogram import filters

from config import ADMINS
from utils.helpers import load_banned, save_banned

def admin_filter(_, __, message):

    return message.from_user.id in ADMINS

admin = filters.create(admin_filter)

def register_admin(app):

    @app.on_message(filters.command("ban") & admin)
    async def ban_user(client, message):

        if len(message.command) < 2:
            return await message.reply_text(
                "Usage: /ban user_id"
            )

        user_id = int(message.command[1])

        banned = load_banned()

        if user_id not in banned:
            banned.append(user_id)

        save_banned(banned)

        await message.reply_text(
            f"Banned: {user_id}"
        )

    @app.on_message(filters.command("unban") & admin)
    async def unban_user(client, message):

        if len(message.command) < 2:
            return await message.reply_text(
                "Usage: /unban user_id"
            )

        user_id = int(message.command[1])

        banned = load_banned()

        if user_id in banned:
            banned.remove(user_id)

        save_banned(banned)

        await message.reply_text(
            f"Unbanned: {user_id}"
        )
