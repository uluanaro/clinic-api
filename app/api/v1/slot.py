from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core.database import get_db
from app.exceptions import SlotNotFoundError
from app.schemas.slot import SlotOut
from app.models.user import User
from app.services.slot_service import SlotService
router = APIRouter(prefix="/slots", tags=["slots"])


@router.get(
    "/{slot_id}",
    response_model=SlotOut,
    status_code=200,
    responses={
        404: {"description": "Слот не найден"},
    },
)
async def get_slot(
        slot_id: int,
        db: AsyncSession = Depends(get_db),
):
    service = SlotService(db)
    try:
        result = await service.get_by_id(slot_id)
    except SlotNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result

@router.get(
    "",
    response_model=list[SlotOut]
)
async def get_all_slots(doctor_id: int, db: AsyncSession = Depends(get_db)):
    service = SlotService(db)
    result = await service.get_all_by_doctor(doctor_id)
    return result



