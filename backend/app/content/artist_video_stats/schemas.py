from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistVideoStatBase(BaseModel):
    artist_video_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class ArtistVideoStatCreate(ArtistVideoStatBase):
    pass

class ArtistVideoStatUpdate(BaseModel):
    artist_video_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class ArtistVideoStatResponse(ArtistVideoStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class ArtistVideoStatList(BaseModel):
    items: list[ArtistVideoStatResponse]
    total: int
    skip: int
    limit: int
