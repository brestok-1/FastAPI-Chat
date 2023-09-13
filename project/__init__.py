from fastapi import FastAPI
from project.config import settings



def create_app() -> FastAPI:
    app = FastAPI()

    from project.users import users_router
    app.include_router(users_router)

    from project.chat import chat_router
    app.include_router(ws_router)

    @app.get('/')
    async def root() -> dict[str, str]:
        return {'message': 'Hello world!'}

    return app
