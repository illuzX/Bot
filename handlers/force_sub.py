from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import (
    FORCE_SUB_CHANNEL,
    FORCE_SUB_LINK
)

async def check_fsub(app, user_id):

    try:

        member = await app.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        return member.status not in [
            "left",
            "kicked"
        ]

    except:
        return False

def join_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Join Channel",
                    url=FORCE_SUB_LINK
                )
            ]
        ]
    )
