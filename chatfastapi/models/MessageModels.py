from typing import List

from pydantic import BaseModel
from datetime import datetime, timezone

class MessageBase(BaseModel):
    text: str
    is_read: bool

class MessageCreate(MessageBase):
    chat_id: int

class MessageRead(MessageBase):
    id: int
    chat_id: int
    user_id: int
    message_time: datetime