from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URI

import certifi

mongo = AsyncIOMotorClient(

    MONGO_URI,

    tls=True,

    tlsCAFile=certifi.where(),

    serverSelectionTimeoutMS=5000

)

db = mongo["gsm_bot"]

solutions = db["solutions"]

users = db["users"]

banned = db["banned"]

settings = db["settings"]


async def add_user(user_id):

    user = await users.find_one({

        "user_id": user_id

    })

    if not user:

        await users.insert_one({

            "user_id": user_id

        })


async def is_banned(user_id):

    user = await banned.find_one({

        "user_id": user_id

    })

    return bool(user)


async def search_solution(query):

    return await solutions.find_one({

        "$or": [

            {

                "model": {

                    "$regex": query,

                    "$options": "i"

                }

            },

            {

                "issue": {

                    "$regex": query,

                    "$options": "i"

                }

            },

            {

                "keywords": {

                    "$regex": query,

                    "$options": "i"

                }

            }

        ]

    })
