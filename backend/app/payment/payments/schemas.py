from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class PaymentBase(BaseModel):
    user_id: int
    payment_type: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    amount: Decimal
    currency: Optional[str] = "KRW"
    status: Optional[Literal["pending", "completed", "failed", "cancelled", "refunded"]] = "pending"
    transaction_id: Optional[str] = None
    payment_method_id: Optional[int] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[Literal["pending", "completed", "failed", "cancelled", "refunded"]] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None

class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class PaymentList(BaseModel):
    items: list[PaymentResponse]
    total: int
    skip: int
    limit: int
