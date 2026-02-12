from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class CalendarSearchBase(BaseModel):
    user_id: int
    search_query: Optional[str] = None
    filters: Optional[dict[str, Any]] = None
    result_count: Optional[int] = 0

class CalendarSearchCreate(CalendarSearchBase):
    pass

class CalendarSearchUpdate(BaseModel):
    search_query: Optional[str] = None
    filters: Optional[dict[str, Any]] = None
    result_count: Optional[int] = None

class CalendarSearchResponse(CalendarSearchBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class CalendarSearchList(BaseModel):
    items: list[CalendarSearchResponse]
    total: int
    skip: int
    limit: int
