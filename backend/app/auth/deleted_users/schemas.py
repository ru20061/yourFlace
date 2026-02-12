from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DeletedUserBase(BaseModel):
    user_id: int
    email: str
    reason: Optional[str] = None
    notes: Optional[str] = None

class DeletedUserCreate(DeletedUserBase):
    scheduled_delete_at: Optional[datetime] = None

class DeletedUserUpdate(BaseModel):
    reason: Optional[str] = None
    notes: Optional[str] = None
    scheduled_delete_at: Optional[datetime] = None

class DeletedUserResponse(DeletedUserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deleted_at: datetime
    scheduled_delete_at: Optional[datetime] = None

class DeletedUserList(BaseModel):
    items: list[DeletedUserResponse]
    total: int
    skip: int
    limit: int
