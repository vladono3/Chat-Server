import json
from datetime import datetime
from uuid import uuid4
from storage.db import db


def create_new_message(message_data):

    messages = db.get_messages()
    message_dict = message_data.model_dump()
    message_id = str(uuid4())

    time = datetime.now()
    hour = time.hour
    date = time.date()
    if len(str(time.minute)) == 1:
        minute = f"0{time.minute}"
    else:
        minute = time.minute

    message_dict["id"] = message_id
    messages[message_id] = message_dict
    message_dict["time"] = f"{date}    {hour}:{minute}"
    message_dict["name"] = "message"

    db.create_message(
        message_id=message_dict["id"],
        discussion_id=message_dict["discussion_id"],
        user_id=message_dict["user_id"],
        value=message_dict["value"],
        created_at=message_dict["time"],
        name=message_dict["name"])

    return message_dict


def get_messages_by_discussion_id(my_user_id, discussion_id):
    messages = db.get_messages()
    users_dict = db.get_users()

    message_list = []
    for key in messages:
        message = messages[key]
        if message.get("discussion_id") == discussion_id:
            user_id = message.get("user_id")
            if user_id == my_user_id:
                message["name"] = "You"
            else:
                message["name"] = users_dict.get(user_id, {}).get("name")
            message_list.append(message)

    return message_list
