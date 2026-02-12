from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriberContentStatBase(BaseModel):
    pass

class SubscriberContentStatCreate(SubscriberContentStatBase):
    pass

class SubscriberContentStatUpdate(BaseModel):
    pass

class SubscriberContentStatResponse(SubscriberContentStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriberContentStatList(BaseModel):
    items: list[SubscriberContentStatResponse]
    total: int
    skip: int
    limit: int
