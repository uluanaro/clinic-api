from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AppointmentCreate(BaseModel):
    slot_id: int
    patient_id: int

class AppointmentOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    slot_id: int
    patient_id: int
    status: str
    created_at: datetime
