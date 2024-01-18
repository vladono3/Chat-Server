from uuid import UUID
from fastapi import HTTPException, APIRouter
from storage.db import db
from users.models import UserCreate

contacts_router = APIRouter()


@contacts_router.get("/api/contacts")
def get_all_contacts():
    users = db.get_users().values()
    return list(users)


@contacts_router.get("/api/contacts/{user_id}", response_model=UserCreate)
def get_contact(user_id: UUID):
    user = db.get_users().get(str(user_id))

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
