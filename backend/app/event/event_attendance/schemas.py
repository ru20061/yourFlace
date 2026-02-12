from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class EventAttendanceBase(BaseModel):
    pass

class EventAttendanceCreate(EventAttendanceBase):
    pass

class EventAttendanceUpdate(BaseModel):
    pass

class EventAttendanceResponse(EventAttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class EventAttendanceList(BaseModel):
    items: list[EventAttendanceResponse]
    total: int
    skip: int
    limit: int
