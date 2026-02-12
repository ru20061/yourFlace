from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ScheduledNotificationBase(BaseModel):
    notification_template_id: int
    receiver_id: int
    send_at: datetime
    is_sent: Optional[bool] = False

class ScheduledNotificationCreate(ScheduledNotificationBase):
    pass

class ScheduledNotificationUpdate(BaseModel):
    send_at: Optional[datetime] = None
    is_sent: Optional[bool] = None
    sent_at: Optional[datetime] = None

class ScheduledNotificationResponse(ScheduledNotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class ScheduledNotificationList(BaseModel):
    items: list[ScheduledNotificationResponse]
    total: int
    skip: int
    limit: int
