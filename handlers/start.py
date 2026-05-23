from pyrogram import filters

def register_start(app):

    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):

        text = '''
Welcome To Mobile Technical Support Bot

Send:
• Mobile Model
• No Display
• No Network
• Charging Issue
• Dead Issue

Example:
Samsung A13 No Network
'''

        await message.reply_text(text)
