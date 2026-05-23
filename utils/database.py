from difflib import SequenceMatcher
from config import DB_CHANNEL

DATABASE = []

async def load_database(app):
    DATABASE.clear()

    async for msg in app.get_chat_history(DB_CHANNEL):

        if not msg.caption:
            continue

        try:
            text = msg.caption.lower()

            model = text.split("model:")[1].split("\n")[0].strip()
            issue = text.split("issue:")[1].split("\n")[0].strip()
            keywords = text.split("keywords:")[1].split("\n")[0].strip()
            solution = text.split("solution:")[1].strip()

            DATABASE.append({
                "model": model,
                "issue": issue,
                "keywords": keywords,
                "solution": solution,
                "photo": msg.photo.file_id if msg.photo else None
            })

        except:
            continue

    print(f"Loaded {len(DATABASE)} Solutions")

async def search_solution(query):

    query = query.lower()

    best_match = None
    best_score = 0

    for item in DATABASE:

        compare_text = f'''
        {item["model"]}
        {item["issue"]}
        {item["keywords"]}
        '''

        score = SequenceMatcher(
            None,
            query,
            compare_text
        ).ratio()

        if score > best_score:
            best_score = score
            best_match = item

    if best_score > 0.40:
        return best_match

    return None
