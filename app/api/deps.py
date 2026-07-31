from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.doctor import Doctor


async def get_existing_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
) -> Doctor:
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Не существует")
    return doctor


@app.post("/doctors/{doctor_id}/slots")
async def create_slot(
        doctor: Doctor = Depends(get_existing_doctor),
):
    return {"message": f"создаём слот для врача {doctor.full_name}"}
