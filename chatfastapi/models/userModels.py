from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    username: str

    model_config = {'from_attributes': True}