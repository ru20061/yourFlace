from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class SubscriptionCancellationBase(BaseModel):
    subscription_id: int
    user_id: int
    artist_id: int
    reason_code: Optional[str] = None
    reason_detail: Optional[str] = None
    subscription_started_at: Optional[datetime] = None
    refund_amount: Optional[Decimal] = None
    is_refunded: bool = False

class SubscriptionCancellationCreate(SubscriptionCancellationBase):
    pass

class SubscriptionCancellationUpdate(BaseModel):
    reason_code: Optional[str] = None
    reason_detail: Optional[str] = None
    refund_amount: Optional[Decimal] = None
    is_refunded: Optional[bool] = None

class SubscriptionCancellationResponse(SubscriptionCancellationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cancelled_at: datetime

class SubscriptionCancellationList(BaseModel):
    items: list[SubscriptionCancellationResponse]
    total: int
    skip: int
    limit: int
