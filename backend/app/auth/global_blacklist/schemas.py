from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class GlobalBlacklistBase(BaseModel):
    admin_id: int
    target_user_id: int
    reason: Optional[str] = None
    status: str = "active"

class GlobalBlacklistCreate(GlobalBlacklistBase):
    pass

class GlobalBlacklistUpdate(BaseModel):
    reason: Optional[str] = None
    status: Optional[str] = None

class GlobalBlacklistResponse(GlobalBlacklistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class GlobalBlacklistList(BaseModel):
    items: list[GlobalBlacklistResponse]
    total: int
    skip: int
    limit: int
