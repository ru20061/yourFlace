from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class UserSettingBase(BaseModel):
    pass

class UserSettingCreate(UserSettingBase):
    pass

class UserSettingUpdate(BaseModel):
    pass

class UserSettingResponse(UserSettingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class UserSettingList(BaseModel):
    items: list[UserSettingResponse]
    total: int
    skip: int
    limit: int
