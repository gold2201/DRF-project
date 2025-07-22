from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from starlette.websockets import WebSocketDisconnect

from db.modelsDB import Chat, User, Message
from depends.chatDepends import get_current_user, get_db
from models.ChatModels import ChatCreate, ChatRead
from models.MessageModels import MessageOut, MessageIn
from models.connectionModel import ConnectionModel

chat = APIRouter()
manager = ConnectionModel()

@chat.get('/chats/my-chats')
async def get_all_chats(current_user: Annotated[User, Depends(get_current_user)], db_session: Annotated[AsyncSession, Depends(get_db)]):
    stmt = (
        select(Chat)
        .options(selectinload(Chat.users))
        .join(Chat.users)
        .where(User.id == current_user.id)
    )

    result = await db_session.execute(stmt)
    chats = result.scalars().all()
    return [ChatRead.model_validate(chat) for chat in chats]

@chat.post("/chats/create-chat")
async def create_chat(
        chat_data: ChatCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_db)]
):
    stmt = select(User).where(User.username == chat_data.second_user_name)
    result = await db_session.execute(stmt)
    second_user = result.scalar_one_or_none()

    if second_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stmt = (
        select(Chat)
        .options(selectinload(Chat.users))
        .join(Chat.users)
        .where(User.id == current_user.id)
    )
    result = await db_session.execute(stmt)
    chats = result.scalars().all()

    for chat in chats:
        if any(user.id == second_user.id for user in chat.users):
            return chat

    new_chat = Chat(name=chat_data.name, users=[current_user, second_user])
    db_session.add(new_chat)
    await db_session.commit()
    await db_session.refresh(new_chat)
    return new_chat

@chat.websocket("/ws/chat/{chat_id}")
async def websocket_chat(
        chat_id: int,
        websocket: WebSocket,
        db_session: Annotated[AsyncSession, Depends(get_db)]):

    token = websocket.query_params.get("token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        current_user = await get_current_user(token, db_session)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    stmt = (
        select(User)
        .join(User.chats)
        .where(Chat.id == chat_id)
    )
    result = await db_session.execute(stmt)
    users = result.scalars().all()
    second_user = next(user for user in users if user.id != current_user.id)

    await manager.connect(chat_id, current_user.id, websocket)

    stmt = (
        update(Message)
        .where(
            Message.chat_id == chat_id,
            Message.is_read == False,
            Message.user_id != current_user.id,
        )
        .values(is_read = True)
    )
    await db_session.execute(stmt)
    await db_session.commit()
    await manager.send_mark_about_read_message(second_user.id, chat_id)

    try:
        while True:
            message = await websocket.receive_json()
            message_in = MessageIn(**message)
            message_out = MessageOut(**message, message_time=datetime.now(timezone.utc))

            new_message = Message(text=message_in.text, message_time=datetime.now(timezone.utc), is_read=False, chat_id=chat_id, user_id=current_user.id)
            db_session.add(new_message)
            await db_session.commit()
            await db_session.refresh(new_message)

            await manager.receive(chat_id, message_out)
            await manager.send_personal_message(second_user.id, chat_id)

    except WebSocketDisconnect:
        await manager.disconnect(chat_id, websocket)

@chat.websocket("/ws/chat/notifications")
async def ws_chat_notification(
        websocket: WebSocket,
        current_user: Annotated[User, Depends(get_current_user)]
):
    await manager.global_connect(current_user.id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.global_disconnect(current_user.id)