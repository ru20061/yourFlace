from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    message: str
    write_id: int
    write_role: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = True

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    write_role: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class NoticeResponse(NoticeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class NoticeList(BaseModel):
    items: list[NoticeResponse]
    total: int
    skip: int
    limit: int
