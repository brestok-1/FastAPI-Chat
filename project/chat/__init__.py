from fastapi import APIRouter

users_router = APIRouter(
    prefix='/chat'
)

from . import models, views
