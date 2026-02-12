from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class EventParticipantBase(BaseModel):
    event_id: int
    user_id: int
    status: Optional[Literal["registered", "cancelled", "attended", "no_show"]] = "registered"

class EventParticipantCreate(EventParticipantBase):
    pass

class EventParticipantUpdate(BaseModel):
    status: Optional[Literal["registered", "cancelled", "attended", "no_show"]] = None
    cancelled_at: Optional[datetime] = None

class EventParticipantResponse(EventParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registered_at: datetime
    cancelled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class EventParticipantList(BaseModel):
    items: list[EventParticipantResponse]
    total: int
    skip: int
    limit: int
