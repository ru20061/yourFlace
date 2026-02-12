from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class CalendarSearchBase(BaseModel):
    pass

class CalendarSearchCreate(CalendarSearchBase):
    pass

class CalendarSearchUpdate(BaseModel):
    pass

class CalendarSearchResponse(CalendarSearchBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class CalendarSearchList(BaseModel):
    items: list[CalendarSearchResponse]
    total: int
    skip: int
    limit: int
