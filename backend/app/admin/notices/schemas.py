from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class NoticeBase(BaseModel):
    pass

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    pass

class NoticeResponse(NoticeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class NoticeList(BaseModel):
    items: list[NoticeResponse]
    total: int
    skip: int
    limit: int
