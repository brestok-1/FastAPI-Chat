from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from project.config import settings
from project.database import get_async_session, async_session_maker
from project.users.auth import auth_backend, fastapi_users
from project.users.schemas import UserRead, UserCreate


def create_app() -> FastAPI:
    app = FastAPI()

    from project.chat import chat_router
    app.include_router(chat_router, tags=['Chat'])

    from project.users import user_router
    app.include_router(user_router, tags=['Users'])

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix='/auth',
        tags=['auth'],
    )

    app.mount('/static', StaticFiles(directory="static"), name="static")

    return app
