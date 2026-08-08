from app.exceptions import SlotNotFoundError
from app.models import Slot
from app.repositories.slot_repository import SlotRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.slot import SlotOut


class SlotService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.slot_repo = SlotRepository(session)

    async def get_by_id(self, slot_id: int) -> Slot:
        result = await self.slot_repo.get_by_id(slot_id)
        if result is None:
            raise SlotNotFoundError(f"Слот {slot_id} не найден")
        return result

    async def get_all_by_doctor(self, doctor_id: int) -> list[Slot]:
        result = await self.slot_repo.get_all_by_doctor(doctor_id)
        return result