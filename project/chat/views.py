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


@chat_router.get('/', name='main')
async def main(request: Request):
    return template.TemplateResponse("welcome.html", {'request': request})


@chat_router.get('/chat', name='chat')
async def print_chat(request: Request,
                     user: User = Depends(current_user)):
    return template.TemplateResponse("main.html", {'request': request, 'username': user.username})


@chat_router.get('/get-messages')
async def get_all_messages(session: AsyncSession = Depends(get_async_session)):
    await asyncio.sleep(1)
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


@chat_router.post('/search')
async def search_messages(text: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Message).where(Message.text == text))
    messages = result.scalars().all()
    return messages


@chat_router.get('/create-message-example')
async def create_message_example(session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, 2)
    message = Message(user=user, username=user.username, text='Hiii')
    session.add(message)
    await session.commit()
    return message
