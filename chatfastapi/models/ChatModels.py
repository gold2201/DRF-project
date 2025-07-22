from typing import List

from pydantic import BaseModel

from models.userModels import UserRead


class Chats(BaseModel):
    name: str

class ChatRead(Chats):
    users: List[UserRead]

    model_config = {'from_attributes': True}

class ChatCreate(Chats):
    second_user_name: str