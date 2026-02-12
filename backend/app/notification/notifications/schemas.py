from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class NotificationBase(BaseModel):
    pass

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    pass

class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class NotificationList(BaseModel):
    items: list[NotificationResponse]
    total: int
    skip: int
    limit: int
