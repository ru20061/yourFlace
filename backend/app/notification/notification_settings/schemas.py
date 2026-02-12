from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NotificationSettingBase(BaseModel):
    subscription_id: Optional[int] = None
    user_id: int
    source_type: Optional[str] = None
    notify_all: Optional[bool] = True
    notify_post: Optional[bool] = True
    notify_comment: Optional[bool] = True
    notify_reply: Optional[bool] = True
    notify_notice: Optional[bool] = True
    notify_payment: Optional[bool] = True
    notify_warning: Optional[bool] = True
    receive_app: Optional[bool] = True
    receive_push: Optional[bool] = True
    receive_email: Optional[bool] = True

class NotificationSettingCreate(NotificationSettingBase):
    pass

class NotificationSettingUpdate(BaseModel):
    source_type: Optional[str] = None
    notify_all: Optional[bool] = None
    notify_post: Optional[bool] = None
    notify_comment: Optional[bool] = None
    notify_reply: Optional[bool] = None
    notify_notice: Optional[bool] = None
    notify_payment: Optional[bool] = None
    notify_warning: Optional[bool] = None
    receive_app: Optional[bool] = None
    receive_push: Optional[bool] = None
    receive_email: Optional[bool] = None

class NotificationSettingResponse(NotificationSettingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class NotificationSettingList(BaseModel):
    items: list[NotificationSettingResponse]
    total: int
    skip: int
    limit: int
