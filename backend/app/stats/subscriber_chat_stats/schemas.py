from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriberChatStatBase(BaseModel):
    pass

class SubscriberChatStatCreate(SubscriberChatStatBase):
    pass

class SubscriberChatStatUpdate(BaseModel):
    pass

class SubscriberChatStatResponse(SubscriberChatStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriberChatStatList(BaseModel):
    items: list[SubscriberChatStatResponse]
    total: int
    skip: int
    limit: int
