from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ErrorLogBase(BaseModel):
    pass

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogUpdate(BaseModel):
    pass

class ErrorLogResponse(ErrorLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ErrorLogList(BaseModel):
    items: list[ErrorLogResponse]
    total: int
    skip: int
    limit: int
