from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class NotificationBase(BaseModel):
    subscription_id: Optional[int] = None
    user_id: int
    noti_type: Literal["content", "social", "event", "order", "chat", "post", "comment", "reply", "notice", "payment", "warning", "system"]
    source_id: Optional[int] = None
    source_type: Optional[str] = None
    event_type: Optional[str] = None
    target_id: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None
    is_read: Optional[bool] = False
    is_pushed: Optional[bool] = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_pushed: Optional[bool] = None

class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class NotificationList(BaseModel):
    items: list[NotificationResponse]
    total: int
    skip: int
    limit: int
