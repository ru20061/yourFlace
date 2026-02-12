from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class EventBase(BaseModel):
    artist_id: int
    title: str
    description: Optional[str] = None
    event_type: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    current_participants: Optional[int] = 0
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    status: Optional[Literal["active", "cancelled", "completed", "full"]] = "active"

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    current_participants: Optional[int] = None
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    status: Optional[Literal["active", "cancelled", "completed", "full"]] = None

class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class EventList(BaseModel):
    items: list[EventResponse]
    total: int
    skip: int
    limit: int
