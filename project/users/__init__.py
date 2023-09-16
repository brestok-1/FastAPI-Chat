from fastapi import APIRouter

from project.users.auth import fastapi_users

current_user = fastapi_users.current_user()

user_router = APIRouter(
    prefix='/user'
)

from project.users import models
