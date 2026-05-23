from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)

from utils.search import smart_search


def register_inline(app):

    @app.on_inline_query()
    async def inline(_, query):

        text = query.query

        if not text:

            return

        data = await smart_search(text)

        results = []

        if data:

            results.append(

                InlineQueryResultArticle(

                    title=data.get("model"),

                    description=data.get("issue"),

                    input_message_content=
                    InputTextMessageContent(

                        f"""
📱 {data.get("model")}

⚠️ {data.get("issue")}

🛠 {data.get("solution")}
"""
                    )
                )
            )

        await query.answer(results)
