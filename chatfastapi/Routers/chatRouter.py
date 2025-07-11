from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.modelsDB import Chat, User
from depends.chatDepends import get_current_user, get_db
from models.ChatModels import ChatCreate, ChatRead

router = APIRouter()

@router.get('/chats')
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

@router.post("/create-chat")
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





































#from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.future import select
#
#from db.db_settings import SessionLocal
#from db.modelsDB import Chat, User
#from models.schemas import ChatCreate  # твоя Pydantic-модель
#
#router = APIRouter()
#
#
## Функция-зависимость для получения БД-сессии
#async def get_db():
#    async with SessionLocal() as session:
#        yield session
#
#
## Эндпоинт создания чата
#@router.post("/chats/")
#async def create_chat(
#    chat_data: ChatCreate,
#    current_user: User = Depends(get_current_user),  # откуда берёшь текущего пользователя
#    db: AsyncSession = Depends(get_db)
#):
#    # 1. Проверка, существует ли пользователь с таким id
#    second_user_stmt = select(User).where(User.id == chat_data.second_user_id)
#    result = await db.execute(second_user_stmt)
#    second_user = result.scalar_one_or_none()
#
#    if not second_user:
#        raise HTTPException(status_code=404, detail="Second user not found")
#
#    # 2. Проверка, существует ли чат между этими двумя пользователями
#    # (упрощённо: получаем все чаты current_user и проверяем, есть ли среди них те, где участвует second_user)
#    for chat in current_user.chats:
#        if second_user in chat.users:
#            return chat  # уже есть чат
#
#    # 3. Создание чата и привязка к двум пользователям
#    new_chat = Chat(name="Chat between users")
#    new_chat.users.append(current_user)
#    new_chat.users.append(second_user)
#
#    db.add(new_chat)
#    await db.commit()
#    await db.refresh(new_chat)
#
#    return new_chat
#