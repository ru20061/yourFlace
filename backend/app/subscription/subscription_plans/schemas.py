from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SubscriptionPlanBase(BaseModel):
    pass

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanUpdate(BaseModel):
    pass

class SubscriptionPlanResponse(SubscriptionPlanBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SubscriptionPlanList(BaseModel):
    items: list[SubscriptionPlanResponse]
    total: int
    skip: int
    limit: int
