from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebImageStatBase(BaseModel):
    celeb_image_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class CelebImageStatCreate(CelebImageStatBase):
    pass

class CelebImageStatUpdate(BaseModel):
    celeb_image_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class CelebImageStatResponse(CelebImageStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class CelebImageStatList(BaseModel):
    items: list[CelebImageStatResponse]
    total: int
    skip: int
    limit: int
