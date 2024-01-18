import json
from uuid import uuid4
from storage.db import db


def get_user_data(user_data):
    users = db.get_users()
    for key in users:
        user = users[key]
        name = user.get("name")
        password = user.get("password")

        if name == user_data.name and password == user_data.password:
            return user

    return None


def create_user(data):
    user_id = str(uuid4())
    user_data = data.model_dump()
    user_data["id"] = user_id

    db.create_user(name=user_data.get("name"), password=user_data.get("password"), user_id=user_id)

    return user_data
