from typing import List

from pydantic import BaseModel
from datetime import datetime, timezone

class UserRead(BaseModel):
    id: int
    username: str

    model_config = {'from_attributes': True}