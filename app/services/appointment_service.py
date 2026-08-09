from app.celery_app import send_appointment_reminder
from app.exceptions import SlotNotFoundError, SlotAlreadyBookedError, PatientNotFoundError
from app.models import User
from sqlalchemy import select
from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.slot_repository import SlotRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.slot_repo = SlotRepository(session)
        self.appointment_repo = AppointmentRepository(session)
        self.user_repo = UserRepository(session)
        self.patient_repo = PatientRepository(session)

    async def book(self, slot_id: int, patient_id: int) -> Appointment:
        slot = await self.slot_repo.get_by_id_for_update(slot_id)
        if slot is None:
            raise SlotNotFoundError(f"Слот {slot_id} не найден")
        appointment = await self.appointment_repo.get_active_by_slot(slot_id)
        if appointment is not None:
            raise SlotAlreadyBookedError()
        patient = await self.patient_repo.get_by_id(patient_id)
        if patient is None:
            raise PatientNotFoundError(f"Пациент с id {patient_id} не найден")
        user = await self.user_repo.get_by_id(patient.user_id)
        email = user.email
        result = await self.appointment_repo.create(slot_id, patient_id)
        slot_time = str(slot.start_time)
        await self.session.commit()
        send_appointment_reminder.delay(email, slot_time)
        return result
