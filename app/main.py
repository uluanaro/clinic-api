from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect

from app.api.v1.appointments import router as appointments_router
from app.api.v1.auth import router as auth_router
from app.api.v1.slot import router as slot_router

from app.websocket_manager import ConnectionManager
import redis.asyncio as redis

from contextlib import asynccontextmanager
import asyncio

manager = ConnectionManager()

async def redis_listener():
    r = redis.from_url("redis://localhost:6379/2", decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("notifications")
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"]
            await manager.broadcast(data)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(redis_listener())
    yield
    task.cancel()

app = FastAPI(title="Clinic API", lifespan=lifespan)

app.include_router(appointments_router)
app.include_router(auth_router)
app.include_router(slot_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            await websocket.send_text(f"The server received message: {msg}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)