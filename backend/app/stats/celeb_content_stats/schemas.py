from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebContentStatBase(BaseModel):
    celeb_id: int
    post_count: Optional[int] = 0
    image_count: Optional[int] = 0
    video_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0
    fan_recommend_count: Optional[int] = 0

class CelebContentStatCreate(CelebContentStatBase):
    pass

class CelebContentStatUpdate(BaseModel):
    post_count: Optional[int] = None
    image_count: Optional[int] = None
    video_count: Optional[int] = None
    fan_like_count: Optional[int] = None
    fan_recommend_count: Optional[int] = None

class CelebContentStatResponse(CelebContentStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime

class CelebContentStatList(BaseModel):
    items: list[CelebContentStatResponse]
    total: int
    skip: int
    limit: int
