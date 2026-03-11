from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebVideoStatBase(BaseModel):
    celeb_video_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class CelebVideoStatCreate(CelebVideoStatBase):
    pass

class CelebVideoStatUpdate(BaseModel):
    celeb_video_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class CelebVideoStatResponse(CelebVideoStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class CelebVideoStatList(BaseModel):
    items: list[CelebVideoStatResponse]
    total: int
    skip: int
    limit: int
