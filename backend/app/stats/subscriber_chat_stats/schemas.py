from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SubscriberChatStatBase(BaseModel):
    subscription_id: int
    messages_sent: Optional[int] = 0
    chat_active_days: Optional[int] = 0

class SubscriberChatStatCreate(SubscriberChatStatBase):
    pass

class SubscriberChatStatUpdate(BaseModel):
    messages_sent: Optional[int] = None
    chat_active_days: Optional[int] = None

class SubscriberChatStatResponse(SubscriberChatStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime

class SubscriberChatStatList(BaseModel):
    items: list[SubscriberChatStatResponse]
    total: int
    skip: int
    limit: int
