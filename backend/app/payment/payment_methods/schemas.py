from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PaymentMethodBase(BaseModel):
    pass

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PaymentMethodList(BaseModel):
    items: list[PaymentMethodResponse]
    total: int
    skip: int
    limit: int
