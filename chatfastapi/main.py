from fastapi import FastAPI

from Routers.chatRouter import router

app = FastAPI()
app.include_router(router)

