from app.schemas.appointment import AppointmentOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.exceptions import SlotNotFoundError, SlotAlreadyBookedError
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    response_model=AppointmentOut,
    status_code=201,
    responses={
        404: {"description": "Слот не найден"},
        409: {"description": "Слот уже занят другим пациентом"},
    },
)
async def create_appointment(
        data: AppointmentCreate,
        db: AsyncSession = Depends(get_db),
):
    service = AppointmentService(db)
    try:
        result = await service.book(data.slot_id, data.patient_id)
    except SlotNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SlotAlreadyBookedError:
        raise HTTPException(status_code=409, detail="Этот слот уже занят")
    return result