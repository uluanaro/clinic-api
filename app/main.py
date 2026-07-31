from fastapi import FastAPI
from app.api.v1.appointments import router as appointments_router

app = FastAPI(title="Clinic API")

app.include_router(appointments_router)