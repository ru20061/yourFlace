from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorImageStatBase(BaseModel):
    creator_image_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class CreatorImageStatCreate(CreatorImageStatBase):
    pass

class CreatorImageStatUpdate(BaseModel):
    creator_image_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class CreatorImageStatResponse(CreatorImageStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class CreatorImageStatList(BaseModel):
    items: list[CreatorImageStatResponse]
    total: int
    skip: int
    limit: int
