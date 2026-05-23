from pyrogram import filters

from config import ADMINS

from utils.database import (
    solutions,
    banned,
    users
)


def register_admin(app):

    @app.on_message(
        filters.command("add") &
        filters.user(ADMINS)
    )
    async def add_solution(_, message):

        try:

            data = message.text.split(
                None,
                1
            )[1]

            parts = data.split("|")

            model = parts[0]
            issue = parts[1]
            keywords = parts[2]
            solution = parts[3]

            photo = None

            if message.reply_to_message:

                if message.reply_to_message.photo:

                    photo = (
                        message.reply_to_message
                        .photo.file_id
                    )

            await solutions.insert_one({

                "model": model,

                "issue": issue,

                "keywords": keywords,

                "solution": solution,

                "photo": photo
            })

            await message.reply(
                "Solution Added."
            )

        except:

            await message.reply(
                """
Usage:

/add model|issue|keywords|solution
"""
            )

    @app.on_message(
        filters.command("ban") &
        filters.user(ADMINS)
    )
    async def ban(_, message):

        if not message.reply_to_message:

            return await message.reply(
                "Reply to user."
            )

        user_id = (
            message.reply_to_message
            .from_user.id
        )

        await banned.insert_one({
            "user_id": user_id
        })

        await message.reply(
            "User banned."
        )

    @app.on_message(
        filters.command("unban") &
        filters.user(ADMINS)
    )
    async def unban(_, message):

        if not message.reply_to_message:

            return await message.reply(
                "Reply to user."
            )

        user_id = (
            message.reply_to_message
            .from_user.id
        )

        await banned.delete_one({
            "user_id": user_id
        })

        await message.reply(
            "User unbanned."
        )

    @app.on_message(
        filters.command("stats") &
        filters.user(ADMINS)
    )
    async def stats(_, message):

        total_users = await users.count_documents({})

        total_solutions = (
            await solutions.count_documents({})
        )

        await message.reply(
            f"""
📊 BOT STATS

👥 USERS:
{total_users}

📱 SOLUTIONS:
{total_solutions}
"""
        )

    @app.on_message(
        filters.command("broadcast") &
        filters.user(ADMINS)
    )
    async def broadcast(_, message):

        try:

            text = message.text.split(
                None,
                1
            )[1]

        except:

            return await message.reply(
                "/broadcast message"
            )

        sent = 0

        async for user in users.find():

            try:

                await app.send_message(
                    user["user_id"],
                    text
                )

                sent += 1

            except:
                pass

        await message.reply(
            f"Broadcast Sent: {sent}"
        )
