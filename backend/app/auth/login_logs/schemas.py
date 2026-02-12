from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class LoginLogBase(BaseModel):
    pass

class LoginLogCreate(LoginLogBase):
    pass

class LoginLogUpdate(BaseModel):
    pass

class LoginLogResponse(LoginLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class LoginLogList(BaseModel):
    items: list[LoginLogResponse]
    total: int
    skip: int
    limit: int
