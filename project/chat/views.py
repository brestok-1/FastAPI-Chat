import asyncio

from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import chat_router
from .models import Message
from project.database import get_async_session
from project.users.models import User
from ..users import current_user

template = Jinja2Templates(directory='project/chat/templates')


@chat_router.get('/chat')
async def print_chat(request: Request):
    return template.TemplateResponse("main.html", {'request': request})


@chat_router.get('/get_messages')
async def get_all_messages(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    await asyncio.sleep(5)
    data = await session.execute(select(Message))
    messages = data.scalars().all()
    return messages


@chat_router.post('/create-message')
async def create_message(text: str,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    message = Message(user=user, user_id=user.id, text=text)
    session.add(message)
    await session.commit()
    return message
