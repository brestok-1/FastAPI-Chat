from fastapi import APIRouter

ws_router = APIRouter(
    prefix='/ws',
    tags=['Ws']
)

from . import views
