from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ProfileBase(BaseModel):
    pass

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    pass

class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ProfileList(BaseModel):
    items: list[ProfileResponse]
    total: int
    skip: int
    limit: int
