from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PostStatBase(BaseModel):
    post_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0
    artist_like_count: Optional[int] = 0

class PostStatCreate(PostStatBase):
    pass

class PostStatUpdate(BaseModel):
    post_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None
    artist_like_count: Optional[int] = None

class PostStatResponse(PostStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class PostStatList(BaseModel):
    items: list[PostStatResponse]
    total: int
    skip: int
    limit: int
