from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    STATUS_SCHEDULED = "scheduled"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    id: Mapped[int] = mapped_column(primary_key=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        Index(
            "uq_appointments_active_slot",
            "slot_id",
            unique=True,
            postgresql_where=(status == STATUS_SCHEDULED),
        ),
    )