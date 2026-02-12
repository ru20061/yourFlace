from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SubscriberContentStatBase(BaseModel):
    subscription_id: int
    post_count: Optional[int] = 0
    image_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0
    fan_recommend_count: Optional[int] = 0

class SubscriberContentStatCreate(SubscriberContentStatBase):
    pass

class SubscriberContentStatUpdate(BaseModel):
    post_count: Optional[int] = None
    image_count: Optional[int] = None
    fan_like_count: Optional[int] = None
    fan_recommend_count: Optional[int] = None

class SubscriberContentStatResponse(SubscriberContentStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime

class SubscriberContentStatList(BaseModel):
    items: list[SubscriberContentStatResponse]
    total: int
    skip: int
    limit: int
