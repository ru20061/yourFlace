from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class UserAddressBase(BaseModel):
    pass

class UserAddressCreate(UserAddressBase):
    pass

class UserAddressUpdate(BaseModel):
    pass

class UserAddressResponse(UserAddressBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class UserAddressList(BaseModel):
    items: list[UserAddressResponse]
    total: int
    skip: int
    limit: int
