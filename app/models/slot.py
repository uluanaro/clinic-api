from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)