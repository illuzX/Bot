from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=False
)

db = client["telegram_bot"]

users = db.users
banned = db.banned


async def add_user(user_id, name):

    user = await users.find_one({"_id": user_id})

    if not user:
        await users.insert_one({
            "_id": user_id,
            "name": name
        })


async def get_users():

    user_list = []

    async for user in users.find():
        user_list.append(user["_id"])

    return user_list


async def total_users():
    return await users.count_documents({})


async def ban_user(user_id):

    already = await banned.find_one({"_id": user_id})

    if not already:
        await banned.insert_one({"_id": user_id})


async def unban_user(user_id):

    await banned.delete_one({"_id": user_id})


async def is_banned(user_id):

    user = await banned.find_one({"_id": user_id})

    return bool(user)