from datetime import datetime

import asyncio
import pytest
import pytest_asyncio

import app.models as models
from app.exceptions import SlotAlreadyBookedError
from app.models import Doctor, User, Patient, Slot, Appointment
from app.services.appointment_service import AppointmentService
from tests.conftest import make_session, session_factory


@pytest.mark.asyncio
async def test_create_appointment(make_session):
    doctor = Doctor(
        id=2,
        full_name="Ivanov II",
    specialization="dentist",
    user_id=2,)
    user = User(id=1, email="test@gmail.com", password_hash="geirgnvjfji", role="patient")
    user2 = User(id=2, email="test2@gmail.com", password_hash="geijfji", role="doctor")
    patient = Patient(id=1, full_name="Uluana", phone="122345", user_id=1)
    slot = Slot(id=1, doctor_id=doctor.id,start_time=datetime.now(), end_time=datetime.now())
    session = make_session
    session.add(user)
    await session.flush()
    session.add(user2)
    await session.flush()
    session.add(doctor)
    await session.flush()
    session.add(slot)
    await session.flush()


    session.add(patient)
    await session.flush()
    await session.commit()

    appointment = await AppointmentService(session).book(slot_id=1, patient_id=1)

    assert appointment.id is not None
    assert appointment.status == Appointment.STATUS_SCHEDULED
    assert appointment.slot_id == 1

@pytest.mark.asyncio
async def test_race_condition_one_wins(session_factory):
    doctor = Doctor(id=2, full_name="Ivanov II", specialization="dentist", user_id=2 )
    user1 = User(id=1, email="test@gmail.com", password_hash="geirgnvjfji", role="patient")
    user2 = User(id=2, email="test2@gmail.com", password_hash="geijfji", role="doctor")
    slot = Slot(id=1, doctor_id=doctor.id,start_time=datetime.now(), end_time=datetime.now())
    patient1 = Patient(id=1, full_name="Uluana", phone="122345", user_id=1)
    patient2 = Patient(id=2, full_name="Artem", phone="1345", user_id=2)
    async with session_factory() as setup:
        setup.add(user1)
        setup.add(user2)
        await setup.flush()
        setup.add(doctor)
        setup.add(patient1)
        setup.add(patient2)
        await setup.flush()
        setup.add(slot)
        await setup.flush()

        await setup.commit()

    async with session_factory() as uluana_s, session_factory() as artem_s:
        coro_uluana = AppointmentService(uluana_s).book(slot_id=1, patient_id=1)
        coro_artem = AppointmentService(artem_s).book(slot_id=1, patient_id=1)
        results = await asyncio.gather(coro_uluana, coro_artem, return_exceptions=True)


    assert sum(1 for r in results if isinstance(r, SlotAlreadyBookedError)) == 1
    assert sum(1 for r in results if isinstance(r, Appointment)) == 1



