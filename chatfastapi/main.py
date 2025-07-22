from fastapi import FastAPI

from Routers.chatRouter import chat

app = FastAPI()
app.include_router(chat)
