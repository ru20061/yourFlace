from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class SubscriptionPlanBase(BaseModel):
    artist_id: int
    name: str
    price: Decimal
    currency: str = "KRW"
    billing_cycle: Literal["monthly", "yearly", "one-time"] = "monthly"
    duration_days: int
    benefits: Optional[str] = None
    is_active: bool = True

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    billing_cycle: Optional[Literal["monthly", "yearly", "one-time"]] = None
    duration_days: Optional[int] = None
    benefits: Optional[str] = None
    is_active: Optional[bool] = None

class SubscriptionPlanResponse(SubscriptionPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class SubscriptionPlanList(BaseModel):
    items: list[SubscriptionPlanResponse]
    total: int
    skip: int
    limit: int
