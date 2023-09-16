from fastapi import APIRouter

chat_router = APIRouter(
    prefix=''
)

from . import models, views
