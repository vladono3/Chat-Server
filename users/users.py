from fastapi import APIRouter
from users.models import UserCreate
from users.utils import get_user_data, create_user

users_router = APIRouter()


@users_router.post("/api/authenticate", response_model=UserCreate)
def authenticate_user(user_data: UserCreate):
    user = get_user_data(user_data)
    if not user:
        user = create_user(user_data)

    return user
