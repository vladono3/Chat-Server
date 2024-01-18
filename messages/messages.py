from fastapi import APIRouter
from fastapi import HTTPException

from messages.models import Messages
from messages.utils import create_new_message, get_messages_by_discussion_id
from storage.db import db
from websocket.manager import ConnectionManager

message_router = APIRouter()


@message_router.post("/api/messages", response_model=Messages)
async def create_message(message_data: Messages):

    discussion_id = message_data.discussion_id
    user_id = message_data.user_id

    discussion = db.get_discussions().get(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found.")

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    message_dict = create_new_message(message_data)
    message_dict["type"] = "message"

    connection_manager = ConnectionManager()
    await connection_manager.broadcast(message_dict, discussion_contacts)

    return message_data


@message_router.get("/api/messages")
def get_message(user_id: str, discussion_id: str):

    discussion = db.get_discussions().get(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found.")

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    return get_messages_by_discussion_id(user_id, discussion_id)
