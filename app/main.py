from fastapi import FastAPI
from app.api.v1.appointments import router as appointments_router
from app.api.v1.auth import router as auth_router
from app.api.v1.slot import router as slot_router

app = FastAPI(title="Clinic API")

app.include_router(appointments_router)
app.include_router(auth_router)
app.include_router(slot_router)