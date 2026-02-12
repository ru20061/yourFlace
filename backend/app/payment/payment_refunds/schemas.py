from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PaymentRefundBase(BaseModel):
    pass

class PaymentRefundCreate(PaymentRefundBase):
    pass

class PaymentRefundUpdate(BaseModel):
    pass

class PaymentRefundResponse(PaymentRefundBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PaymentRefundList(BaseModel):
    items: list[PaymentRefundResponse]
    total: int
    skip: int
    limit: int
