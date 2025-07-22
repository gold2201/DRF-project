from pydantic import BaseModel
from datetime import datetime

class MessageIn(BaseModel):
    text: str

class MessageOut(MessageIn):
    message_time: datetime