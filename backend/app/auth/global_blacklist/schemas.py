from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class GlobalBlacklistBase(BaseModel):
    pass

class GlobalBlacklistCreate(GlobalBlacklistBase):
    pass

class GlobalBlacklistUpdate(BaseModel):
    pass

class GlobalBlacklistResponse(GlobalBlacklistBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class GlobalBlacklistList(BaseModel):
    items: list[GlobalBlacklistResponse]
    total: int
    skip: int
    limit: int
