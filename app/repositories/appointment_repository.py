from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.appointment import Appointment

class AppointmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, slot_id: int, patient_id: int) -> Appointment:
        appointment = Appointment(slot_id=slot_id, patient_id=patient_id, status=Appointment.STATUS_SCHEDULED)
        self.session.add(appointment)
        await self.session.flush()
        return appointment

    async def get_active_by_slot(self, slot_id: int) -> Appointment | None:
        result = await self.session.execute(select(Appointment).where(Appointment.slot_id == slot_id, Appointment.status == Appointment.STATUS_SCHEDULED))
        return result.scalar_one_or_none()