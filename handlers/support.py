from pyrogram import filters

from utils.database import search_solution
from utils.logger import log_query
from utils.helpers import is_banned

from handlers.force_sub import (
    check_fsub,
    join_button
)

def register_support(app):

    @app.on_message(
        filters.private &
        filters.text
    )
    async def support_system(client, message):

        user = message.from_user
        query = message.text

        if is_banned(user.id):

            return await message.reply_text(
                "You are banned from using this bot."
            )

        joined = await check_fsub(
            client,
            user.id
        )

        if not joined:

            return await message.reply_text(
                "Please join our updates channel first.",
                reply_markup=join_button()
            )

        result = await search_solution(query)

        if not result:

            reply = '''
No Solution Found.

Try:
• Exact Model
• Exact Complaint
• Detailed Query
'''

            await message.reply_text(reply)

            await log_query(
                client,
                user,
                query,
                reply
            )

            return

        solution = result["solution"]

        if result["photo"]:

            await message.reply_photo(
                result["photo"],
                caption=solution
            )

        else:

            await message.reply_text(solution)

        await log_query(
            client,
            user,
            query,
            solution
        )
