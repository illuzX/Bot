from pyrogram import Client
from flask import Flask
from threading import Thread
import asyncio
import uvloop

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)

uvloop.install()

web = Flask(__name__)


@web.route("/")
def home():
    return "Bot Running ✅"


def run_web():
    web.run(
        host="0.0.0.0",
        port=8000
    )


bot = Client(
    "AdvancedBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)


async def main():

    await bot.start()

    me = await bot.get_me()

    print(f"{me.first_name} Started ✅")

    await asyncio.Event().wait()


if __name__ == "__main__":

    Thread(target=run_web).start()

    asyncio.run(main())