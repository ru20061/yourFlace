from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class UserList(BaseModel):
    items: list[UserResponse]
    total: int
    skip: int
    limit: int
