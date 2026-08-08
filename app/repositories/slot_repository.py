from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.slot import Slot
from sqlalchemy import select

class SlotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, doctor_id: int, start_time: datetime, end_time: datetime) -> Slot:
        slot = Slot(doctor_id=doctor_id, start_time=start_time, end_time=end_time)
        self.session.add(slot)
        await self.session.flush()
        return slot

    async def get_by_id_for_update(self, slot_id: int) -> Slot | None:
        result = await self.session.execute(
            select(Slot).where(Slot.id == slot_id).with_for_update())
        return result.scalar_one_or_none()

    async def get_all_by_doctor(self, doctor_id: int) -> list[Slot]:
        result = await self.session.execute(
            select(Slot).where(Slot.doctor_id == doctor_id)
        )
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Slot | None:
        result = await self.session.execute(
            select(Slot).where(Slot.id == id)
        )
        return result.scalar_one_or_none()
