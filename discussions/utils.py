from collections import Counter
from uuid import uuid4
from storage.db import db


def get_contact_discussions(data):
    discussions = db.get_discussions().values()
    for discussion in discussions:
        contact_id = discussion.get("contacts")
        if Counter(contact_id) == Counter(data):
            return discussion
    return None


def create_new_discussion(data):

    discussion_id = str(uuid4())
    discussion_data = data.model_dump()
    discussion_data["id"] = discussion_id

    db.create_discussion(contacts=discussion_data["contacts"], discussion_id=discussion_data["id"], name=discussion_data["name"])

    return discussion_data


def get_discussions(user_id):
    discussion_list = []
    discussions = db.get_discussions()

    for discussion_key in discussions:
        discussion = discussions[discussion_key]
        contacts = discussion.get("contacts", [])
        if user_id in contacts:
            discussion_list.append(discussion)
    return discussion_list
