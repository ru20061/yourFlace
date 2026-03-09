from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorVideoStatBase(BaseModel):
    creator_video_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class CreatorVideoStatCreate(CreatorVideoStatBase):
    pass

class CreatorVideoStatUpdate(BaseModel):
    creator_video_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class CreatorVideoStatResponse(CreatorVideoStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class CreatorVideoStatList(BaseModel):
    items: list[CreatorVideoStatResponse]
    total: int
    skip: int
    limit: int
