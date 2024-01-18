from fastapi import APIRouter
from fastapi import HTTPException

from discussions.models import Discussions
from discussions.utils import get_contact_discussions, create_new_discussion, get_discussions
from storage.db import db

discussions_router = APIRouter()


@discussions_router.post("/api/discussions")
def create_discussion(discussion_data: Discussions):
    contacts = discussion_data.contacts

    users = db.get_users()
    for contact in contacts:
        if users.get(str(contact)) is None:
            raise HTTPException(status_code=404, detail="Contact not found.")

    # contacts = remove_duplicate_contacts(contacts)
    contacts_discussions = get_contact_discussions(contacts)

    if contacts_discussions:
        raise HTTPException(status_code=404, detail="Discussion Already exists.")

    contacts_discussion = create_new_discussion(discussion_data)
    return contacts_discussion


@discussions_router.get("/api/discussions")
def get_discussion(user_id: str = None):
    if user_id is None:
        discussions = db.get_discussions().values()
        return list(discussions)

    return get_discussions(user_id)


