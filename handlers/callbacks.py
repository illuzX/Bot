from pyrogram import filters


def register_callbacks(app):

    @app.on_callback_query()
    async def callbacks(_, query):

        data = query.data

        if data == "common":

            await query.message.reply(
                """
📚 COMMON ISSUES

• No Network
• Charging
• Dead
• Restart
• Heating
• Bootloop
• Camera
• Wifi
"""
            )
