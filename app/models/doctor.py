from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Doctor(Base):
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    specialization: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

