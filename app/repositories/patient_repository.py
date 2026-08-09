from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.patient import Patient
from sqlalchemy import select

class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.id == id)
        )
        return result.scalar_one_or_none()