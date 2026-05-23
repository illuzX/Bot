from config import LOG_CHANNEL

async def log_query(app, user, query, reply):

    text = f'''
#NEW_QUERY

👤 User:
{user.mention}

🆔 ID:
{user.id}

📩 Query:
{query}

🤖 Reply:
{reply}
'''

    await app.send_message(LOG_CHANNEL, text)
