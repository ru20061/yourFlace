from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    pass

class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class OrderList(BaseModel):
    items: list[OrderResponse]
    total: int
    skip: int
    limit: int
