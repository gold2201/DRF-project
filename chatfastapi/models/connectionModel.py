from typing import Dict, List, Tuple

from fastapi import WebSocket

from models.MessageModels import MessageOut

class ConnectionModel:
    def __init__(self):
        self.global_active_connections: Dict[int, WebSocket] = {}
        self.active_connections_in_chat: Dict[int, List[Tuple[int, WebSocket]]] = {}

    async def global_connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.global_active_connections[user_id] = websocket

    async def connect(self, chat_id: int, user_id, websocket: WebSocket):
        await websocket.accept()
        self.active_connections_in_chat.setdefault(chat_id, []).append((user_id, websocket))

    def global_disconnect(self, user_id: int):
        self.global_active_connections.pop(user_id, None)

    async def disconnect(self, chat_id: int, websocket: WebSocket):
        connections = self.active_connections_in_chat.get(chat_id, [])
        self.active_connections_in_chat[chat_id] = [(uid, ws) for uid, ws in connections if ws != websocket]

    async def send_personal_message(self, user_id: int, message_chat_id: int):
        websocket = self.global_active_connections.get(user_id)
        if websocket:
            await websocket.send_text(str(message_chat_id))

    async def receive(self, chat_id: int, message: MessageOut):
        for _, websocket in self.active_connections_in_chat.get(chat_id, []):
            await websocket.send_text(message.model_dump_json())

    async def send_mark_about_read_message(self, user_id: int, chat_id: int):
        for uid, websocket in self.active_connections_in_chat.get(chat_id, []):
            if uid == user_id:
                await websocket.send_text(str(chat_id))


