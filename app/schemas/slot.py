from pydantic import BaseModel, ConfigDict
from datetime import datetime



class SlotOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime