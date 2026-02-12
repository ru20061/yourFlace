from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class EventParticipantBase(BaseModel):
    pass

class EventParticipantCreate(EventParticipantBase):
    pass

class EventParticipantUpdate(BaseModel):
    pass

class EventParticipantResponse(EventParticipantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class EventParticipantList(BaseModel):
    items: list[EventParticipantResponse]
    total: int
    skip: int
    limit: int
