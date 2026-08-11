from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect

from app.api.v1.appointments import router as appointments_router
from app.api.v1.auth import router as auth_router
from app.api.v1.slot import router as slot_router

app = FastAPI(title="Clinic API")

app.include_router(appointments_router)
app.include_router(auth_router)
app.include_router(slot_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            await websocket.send_text(f"The server received message: {msg}")
    except WebSocketDisconnect:
        print("A client left the server")