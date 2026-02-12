from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class DeletedUserBase(BaseModel):
    pass

class DeletedUserCreate(DeletedUserBase):
    pass

class DeletedUserUpdate(BaseModel):
    pass

class DeletedUserResponse(DeletedUserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class DeletedUserList(BaseModel):
    items: list[DeletedUserResponse]
    total: int
    skip: int
    limit: int
