from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriptionBase(BaseModel):
    pass

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    pass

class SubscriptionResponse(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriptionList(BaseModel):
    items: list[SubscriptionResponse]
    total: int
    skip: int
    limit: int
