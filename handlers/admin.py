from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import *

from utils.database import (
    add_user,
    is_banned
)


def register_start(app):

    @app.on_message(
        filters.command("start")
    )
    async def start(_, message):

        user_id = message.from_user.id

        if await is_banned(user_id):

            return await message.reply(
                "You are banned."
            )

        try:

            member = await app.get_chat_member(
                FORCE_SUB_CHANNEL,
                user_id
            )

            if member.status in [
                "left",
                "kicked"
            ]:
                raise Exception

        except:

            return await message.reply(
                "Join channel first.",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "Join Channel",
                            url=FORCE_SUB_LINK
                        )
                    ]]
                )
            )

        await add_user(user_id)

        buttons = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📚 Common Issues",
                    callback_data="common"
                )
            ],

            [
                InlineKeyboardButton(
                    "📞 Admin",
                    url="https://t.me/yourusername"
                )
            ]

        ])

        await message.reply(
            """
📱 Advanced GSM Technical Support Bot

Send:
• Mobile Model
• Complaint
• Board Issue
• PMIC Issue
• Signal Issue
""",
            reply_markup=buttons
        )
