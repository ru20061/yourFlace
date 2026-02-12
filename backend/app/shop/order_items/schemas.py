from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class OrderItemBase(BaseModel):
    pass

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    pass

class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class OrderItemList(BaseModel):
    items: list[OrderItemResponse]
    total: int
    skip: int
    limit: int
