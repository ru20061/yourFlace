from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class ArtistVideoBase(BaseModel):
    artist_id: int
    write_id: int
    write_role: Literal["artist", "manager"]
    url: str
    thumbnail_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = "public"
    is_visible: Optional[bool] = True
    search_text: Optional[str] = None

class ArtistVideoCreate(ArtistVideoBase):
    pass

class ArtistVideoUpdate(BaseModel):
    artist_id: Optional[int] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["artist", "manager"]] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = None
    is_visible: Optional[bool] = None
    search_text: Optional[str] = None

class ArtistVideoResponse(ArtistVideoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ArtistVideoList(BaseModel):
    items: list[ArtistVideoResponse]
    total: int
    skip: int
    limit: int
