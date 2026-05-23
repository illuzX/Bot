DATABASE = []


async def load_database(app):

    print("Database Ready")


async def add_solution(
    model,
    issue,
    keywords,
    solution,
    photo=None
):

    DATABASE.append({
        "model": model.lower(),
        "issue": issue.lower(),
        "keywords": keywords.lower(),
        "solution": solution,
        "photo": photo
    })


async def search_solution(query):

    query = query.lower()

    for item in DATABASE:

        compare = f"""
        {item['model']}
        {item['issue']}
        {item['keywords']}
        """

        if query in compare:
            return item

    return None
