from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class FAQBase(BaseModel):
    pass

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    pass

class FAQResponse(FAQBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class FAQList(BaseModel):
    items: list[FAQResponse]
    total: int
    skip: int
    limit: int
