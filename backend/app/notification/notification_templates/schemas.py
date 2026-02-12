from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class NotificationTemplateBase(BaseModel):
    pass

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(BaseModel):
    pass

class NotificationTemplateResponse(NotificationTemplateBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class NotificationTemplateList(BaseModel):
    items: list[NotificationTemplateResponse]
    total: int
    skip: int
    limit: int
