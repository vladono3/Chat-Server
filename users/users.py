from fastapi import APIRouter
from users.models import UserCreate
from users.utils import get_user_data, create_user
from storage.db import db
users_router = APIRouter()

@users_router.get("/api/users")
def get_user(user_id: str = None):
    if user_id is None:
        discussions = db.get_users().values()
        return list(discussions)

    return get_user(user_id)
@users_router.post("/api/authenticate", response_model=UserCreate)
def authenticate_user(user_data: UserCreate):
    user = get_user_data(user_data)
    if not user:
        user = create_user(user_data)

    return user
