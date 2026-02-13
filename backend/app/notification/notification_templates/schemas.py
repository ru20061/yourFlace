from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class NotificationTemplateBase(BaseModel):
    template_name: str
    noti_type: Literal["content", "social", "event", "order", "chat", "post", "comment", "reply", "notice", "payment", "warning", "system"]
    title_template: Optional[str] = None
    message_template: Optional[str] = None
    is_active: Optional[bool] = True

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    noti_type: Optional[Literal["post", "comment", "reply", "notice", "payment", "warning", "system"]] = None
    title_template: Optional[str] = None
    message_template: Optional[str] = None
    is_active: Optional[bool] = None

class NotificationTemplateResponse(NotificationTemplateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class NotificationTemplateList(BaseModel):
    items: list[NotificationTemplateResponse]
    total: int
    skip: int
    limit: int
