from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class OrderBase(BaseModel):
    user_id: int
    order_number: str
    total_amount: Decimal
    currency: Optional[str] = "KRW"
    status: Optional[Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"]] = "pending"
    payment_id: Optional[int] = None
    shipping_address_id: Optional[int] = None
    tracking_number: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"]] = None
    payment_id: Optional[int] = None
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class OrderList(BaseModel):
    items: list[OrderResponse]
    total: int
    skip: int
    limit: int
