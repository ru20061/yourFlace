from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime, date
from decimal import Decimal

class SubscriptionBase(BaseModel):
    fan_id: int
    artist_id: int
    fan_nickname: Optional[str] = None
    fan_profile_image: Optional[str] = None
    status: Literal["subscribed", "cancelled", "expired"] = "subscribed"
    payments_type: Literal["free", "paid"] = "free"
    start_date: date
    end_date: Optional[date] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    fan_nickname: Optional[str] = None
    fan_profile_image: Optional[str] = None
    status: Optional[Literal["subscribed", "cancelled", "expired"]] = None
    payments_type: Optional[Literal["free", "paid"]] = None
    end_date: Optional[date] = None

class SubscriptionResponse(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class SubscriptionList(BaseModel):
    items: list[SubscriptionResponse]
    total: int
    skip: int
    limit: int
