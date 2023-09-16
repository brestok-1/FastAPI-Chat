from fastapi import FastAPI, Depends
from project.config import settings
from project.users.auth import auth_backend, fastapi_users
from project.users.schemas import UserRead, UserCreate


def create_app() -> FastAPI:
    app = FastAPI()

    from project.chat import chat_router
    app.include_router(chat_router)

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

    @app.get('/')
    async def root() -> dict[str, str]:
        return {'message': 'Hello world!'}
    current_user = fastapi_users.current_user()
    @app.get('/protected')
    def protected_route(user = Depends(current_user)):
        return f'Hello, {user.username}'

    @app.get('/unprotected')
    def unprotected_route():
        return 'Hi, anonymous!'
    return app
