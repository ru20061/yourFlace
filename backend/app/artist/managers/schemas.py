from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ManagerBase(BaseModel):
    user_id: int
    artist_id: int
    role: str = "manager"
    status: str = "active"

class ManagerCreate(ManagerBase):
    pass

class ManagerUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None

class ManagerResponse(ManagerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ManagerList(BaseModel):
    items: list[ManagerResponse]
    total: int
    skip: int
    limit: int
