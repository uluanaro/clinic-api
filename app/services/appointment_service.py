from app.exceptions import SlotNotFoundError, SlotAlreadyBookedError
from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.slot_repository import SlotRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.slot_repo = SlotRepository(session)
        self.appointment_repo = AppointmentRepository(session)

    async def book(self, slot_id: int, patient_id: int) -> Appointment:
        slot = await self.slot_repo.get_by_id_for_update(slot_id)
        if slot is None:
            raise SlotNotFoundError(f"Слот {slot_id} не найден")
        appointment = await self.appointment_repo.get_active_by_slot(slot_id)
        if appointment is not None:
            raise SlotAlreadyBookedError()
        result = await self.appointment_repo.create(slot_id, patient_id)
        await self.session.commit()
        return result
