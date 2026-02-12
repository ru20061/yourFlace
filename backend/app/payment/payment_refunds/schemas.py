from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class PaymentRefundBase(BaseModel):
    payment_id: int
    user_id: int
    refund_amount: Decimal
    reason: Optional[str] = None
    status: Optional[Literal["pending", "approved", "rejected", "completed"]] = "pending"

class PaymentRefundCreate(PaymentRefundBase):
    pass

class PaymentRefundUpdate(BaseModel):
    reason: Optional[str] = None
    status: Optional[Literal["pending", "approved", "rejected", "completed"]] = None
    processed_at: Optional[datetime] = None

class PaymentRefundResponse(PaymentRefundBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class PaymentRefundList(BaseModel):
    items: list[PaymentRefundResponse]
    total: int
    skip: int
    limit: int
