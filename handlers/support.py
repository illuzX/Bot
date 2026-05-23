from pyrogram import filters

from config import LOG_CHANNEL

from utils.database import (
    is_banned
)

from utils.search import smart_search

from utils.cache import CACHE

from utils.spam import anti_spam


def register_support(app):

    @app.on_message(
        filters.text &
        ~filters.command([
            "start",
            "add",
            "ban",
            "unban",
            "stats",
            "broadcast"
        ])
    )
    async def support(_, message):

        user_id = message.from_user.id

        if not anti_spam(user_id):

            return await message.reply(
                "Slow down."
            )

        if await is_banned(user_id):

            return await message.reply(
                "You are banned."
            )

        query = message.text

        if query in CACHE:

            data = CACHE[query]

        else:

            data = await smart_search(query)

            CACHE[query] = data

        if not data:

            reply = """
❌ No solution found.

Try:
• Exact model
• Short complaint
• Different keyword
"""

            await message.reply(reply)

        else:

            text = f"""
📱 Model:
{data.get("model")}

⚠️ Issue:
{data.get("issue")}

🛠 Solution:
{data.get("solution")}
"""

            if data.get("photo"):

                await message.reply_photo(
                    data["photo"],
                    caption=text
                )

            else:

                await message.reply(text)

            reply = text

        await app.send_message(
            LOG_CHANNEL,
            f"""
👤 USER:
{message.from_user.mention}

📩 QUERY:
{query}

🤖 REPLY:
{reply}
"""
        )
