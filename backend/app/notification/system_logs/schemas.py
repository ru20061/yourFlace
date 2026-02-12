from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SystemLogBase(BaseModel):
    pass

class SystemLogCreate(SystemLogBase):
    pass

class SystemLogUpdate(BaseModel):
    pass

class SystemLogResponse(SystemLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SystemLogList(BaseModel):
    items: list[SystemLogResponse]
    total: int
    skip: int
    limit: int
