from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SystemMessageBase(BaseModel):
    title: str
    message: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    write_id: int

class SystemMessageCreate(SystemMessageBase):
    pass

class SystemMessageUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class SystemMessageResponse(SystemMessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class SystemMessageList(BaseModel):
    items: list[SystemMessageResponse]
    total: int
    skip: int
    limit: int
