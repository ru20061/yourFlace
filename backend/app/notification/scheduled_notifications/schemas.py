from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ScheduledNotificationBase(BaseModel):
    pass

class ScheduledNotificationCreate(ScheduledNotificationBase):
    pass

class ScheduledNotificationUpdate(BaseModel):
    pass

class ScheduledNotificationResponse(ScheduledNotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ScheduledNotificationList(BaseModel):
    items: list[ScheduledNotificationResponse]
    total: int
    skip: int
    limit: int
