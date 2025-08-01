from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routers.chatRouter import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat)