from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class UserDeviceBase(BaseModel):
    pass

class UserDeviceCreate(UserDeviceBase):
    pass

class UserDeviceUpdate(BaseModel):
    pass

class UserDeviceResponse(UserDeviceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class UserDeviceList(BaseModel):
    items: list[UserDeviceResponse]
    total: int
    skip: int
    limit: int
