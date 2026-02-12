from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriptionCancellationBase(BaseModel):
    pass

class SubscriptionCancellationCreate(SubscriptionCancellationBase):
    pass

class SubscriptionCancellationUpdate(BaseModel):
    pass

class SubscriptionCancellationResponse(SubscriptionCancellationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriptionCancellationList(BaseModel):
    items: list[SubscriptionCancellationResponse]
    total: int
    skip: int
    limit: int
