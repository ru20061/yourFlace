from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ChatReportBase(BaseModel):
    chat_message_id: int
    reported_by: int
    reason: Optional[str] = None
    status: Optional[Literal["pending", "reviewed", "resolved", "rejected"]] = "pending"

class ChatReportCreate(ChatReportBase):
    pass

class ChatReportUpdate(BaseModel):
    reason: Optional[str] = None
    status: Optional[Literal["pending", "reviewed", "resolved", "rejected"]] = None

class ChatReportResponse(ChatReportBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ChatReportList(BaseModel):
    items: list[ChatReportResponse]
    total: int
    skip: int
    limit: int
