from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None

class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class OrderItemList(BaseModel):
    items: list[OrderItemResponse]
    total: int
    skip: int
    limit: int
