from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_websockets: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_websockets.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_websockets.remove(websocket)

    async def broadcast(self, message: str):
        for websocket in self.active_websockets:
            await websocket.send_text(message)

