from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class NotificationSettingBase(BaseModel):
    pass

class NotificationSettingCreate(NotificationSettingBase):
    pass

class NotificationSettingUpdate(BaseModel):
    pass

class NotificationSettingResponse(NotificationSettingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class NotificationSettingList(BaseModel):
    items: list[NotificationSettingResponse]
    total: int
    skip: int
    limit: int
