from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriptionBlacklistBase(BaseModel):
    pass

class SubscriptionBlacklistCreate(SubscriptionBlacklistBase):
    pass

class SubscriptionBlacklistUpdate(BaseModel):
    pass

class SubscriptionBlacklistResponse(SubscriptionBlacklistBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriptionBlacklistList(BaseModel):
    items: list[SubscriptionBlacklistResponse]
    total: int
    skip: int
    limit: int
