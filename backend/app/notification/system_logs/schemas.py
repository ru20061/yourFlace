from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class SystemLogBase(BaseModel):
    scheduled_notification_id: Optional[int] = None
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    channel: Optional[Literal["app", "push", "email", "sms"]] = None
    status: Literal["success", "failed", "pending", "delivered"]
    error_message: Optional[str] = None

class SystemLogCreate(SystemLogBase):
    pass

class SystemLogUpdate(BaseModel):
    status: Optional[Literal["success", "failed", "pending"]] = None
    error_message: Optional[str] = None

class SystemLogResponse(SystemLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class SystemLogList(BaseModel):
    items: list[SystemLogResponse]
    total: int
    skip: int
    limit: int
