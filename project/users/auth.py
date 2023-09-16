import os

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from project.users.manager import get_user_manager
from project.users.models import User

cookie_transport = CookieTransport(cookie_name="livechat", cookie_max_age=3600)


def get_jwt_stategy() -> JWTStrategy:
    return JWTStrategy(secret=os.getenv('SECRET'), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_stategy
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


