from rapidfuzz import fuzz

from utils.database import solutions


async def smart_search(query):

    best = None

    highest = 0

    async for data in solutions.find():

        text = f"""
        {data.get("model","")}
        {data.get("issue","")}
        {data.get("keywords","")}
        """

        score = fuzz.partial_ratio(
            query.lower(),
            text.lower()
        )

        if score > highest:

            highest = score

            best = data

    if highest >= 60:

        return best

    return None
