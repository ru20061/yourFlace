from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EventAttendanceBase(BaseModel):
    event_id: int
    participant_id: int
    checked_in_by: Optional[int] = None

class EventAttendanceCreate(EventAttendanceBase):
    pass

class EventAttendanceUpdate(BaseModel):
    checked_in_by: Optional[int] = None

class EventAttendanceResponse(EventAttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    checked_in_at: datetime

class EventAttendanceList(BaseModel):
    items: list[EventAttendanceResponse]
    total: int
    skip: int
    limit: int
