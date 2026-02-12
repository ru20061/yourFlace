from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SystemMessageBase(BaseModel):
    pass

class SystemMessageCreate(SystemMessageBase):
    pass

class SystemMessageUpdate(BaseModel):
    pass

class SystemMessageResponse(SystemMessageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SystemMessageList(BaseModel):
    items: list[SystemMessageResponse]
    total: int
    skip: int
    limit: int
