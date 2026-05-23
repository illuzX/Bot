import json
import os

BAN_FILE = "banned.json"

def load_banned():

    if not os.path.exists(BAN_FILE):
        return []

    with open(BAN_FILE, "r") as f:
        return json.load(f)

def save_banned(data):

    with open(BAN_FILE, "w") as f:
        json.dump(data, f)

def is_banned(user_id):

    return user_id in load_banned()
