from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PaymentBase(BaseModel):
    pass

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    pass

class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PaymentList(BaseModel):
    items: list[PaymentResponse]
    total: int
    skip: int
    limit: int
