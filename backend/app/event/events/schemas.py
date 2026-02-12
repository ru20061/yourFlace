from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class EventBase(BaseModel):
    pass

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    pass

class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class EventList(BaseModel):
    items: list[EventResponse]
    total: int
    skip: int
    limit: int
