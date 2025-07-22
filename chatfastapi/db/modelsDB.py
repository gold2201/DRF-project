from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .db_settings import Base

chat_user_association = Table(
    "chat_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey('auth_user.id'), primary_key=True),
    Column("chat_id", Integer, ForeignKey('chats.id'), primary_key=True),
)

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    chats = relationship("Chat", secondary=chat_user_association, back_populates="users")
    messages = relationship("Message", back_populates="user", cascade="all, delete")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship("User", secondary=chat_user_association, back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete")

class Message(Base):
    __tablename__ = name__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    message_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_read = Column(Boolean,default=False)

    user_id = Column(Integer, ForeignKey("auth_user.id"), index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), index=True)

    user = relationship("User", back_populates='messages')
    chat = relationship("Chat", back_populates="messages")




