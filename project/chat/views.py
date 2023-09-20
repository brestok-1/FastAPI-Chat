import asyncio

from fastapi import Depends, WebSocket
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from . import chat_router
from .models import Message
from project.database import get_async_session
from project.users.models import User
from .schemas import MessageCreate
from ..users import current_user
from ..ws.views import manager

template = Jinja2Templates(directory='project/chat/templates')


@chat_router.get('/', name='main')
async def main(request: Request):
    return template.TemplateResponse("welcome.html", {'request': request})


@chat_router.get('/chat', name='chat')
async def print_chat(request: Request,
                     user: User = Depends(current_user)):
    return template.TemplateResponse("main.html", {'request': request, 'username': user.username})


@chat_router.get('/get-messages')
async def get_all_messages(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    await asyncio.sleep(1)
    first_message_id = user.first_message_id
    if first_message_id is None:
        last_message = await session.execute(select(Message).order_by(desc(Message.id)).limit(1))
        last_message = last_message.first()
        if last_message:
            last_message = last_message[0]
            if last_message.id >= 10:
                first_message = await session.execute(select(Message).filter(Message.id == last_message.id - 10))
                first_message = first_message.scalar_one()
                first_message_id = first_message.id
            else:
                first_message = await session.execute(select(Message))
                first_message = first_message.first()
                first_message_id = first_message[0].id
            user.first_message_id = first_message_id
            session.add(user)
        else:
            first_message_id = 1
            user.first_message_id = first_message_id
            session.add(user)
    data = await session.execute(select(Message).filter(Message.id > first_message_id))
    messages = data.scalars().all()
    messages = [message.as_dict() for message in messages]
    await session.commit()
    return messages


@chat_router.post('/create-message')
async def create_message(message_data: MessageCreate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    message = Message(user=user, username=user.username, text=message_data.text)
    session.add(message)
    await session.commit()
    return message


@chat_router.get('/search')
async def search_messages(text: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Message).where(func.lower(Message.text).ilike(f"%{text.lower()}%")))
    messages = result.scalars().all()
    return messages


@chat_router.get('/example')
async def get_all_messages(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    first_message_id = user.first_message_id
    print(first_message_id)
    print(first_message_id)
    print(first_message_id)
    print(first_message_id)
    print(first_message_id)
    print(first_message_id)
    return {'hi' : first_message_id}
