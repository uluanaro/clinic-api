from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
