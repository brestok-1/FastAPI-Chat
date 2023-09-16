from fastapi import APIRouter

chat_router = APIRouter(
    prefix='/chat'
)

from . import models, views
