from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistImageStatBase(BaseModel):
    artist_image_id: int
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    fan_like_count: Optional[int] = 0

class ArtistImageStatCreate(ArtistImageStatBase):
    pass

class ArtistImageStatUpdate(BaseModel):
    artist_image_id: Optional[int] = None
    view_count: Optional[int] = None
    comment_count: Optional[int] = None
    fan_like_count: Optional[int] = None

class ArtistImageStatResponse(ArtistImageStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None

class ArtistImageStatList(BaseModel):
    items: list[ArtistImageStatResponse]
    total: int
    skip: int
    limit: int
