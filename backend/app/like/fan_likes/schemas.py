from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class FanLikeBase(BaseModel):
    pass

class FanLikeCreate(FanLikeBase):
    pass

class FanLikeUpdate(BaseModel):
    pass

class FanLikeResponse(FanLikeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class FanLikeList(BaseModel):
    items: list[FanLikeResponse]
    total: int
    skip: int
    limit: int
