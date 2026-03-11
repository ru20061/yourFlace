from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class CelebVideoBase(BaseModel):
    celeb_id: int
    write_id: int
    write_role: Literal["celeb", "manager", "artist"]
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

class CelebVideoCreate(CelebVideoBase):
    pass

class CelebVideoUpdate(BaseModel):
    celeb_id: Optional[int] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["celeb", "manager", "artist"]] = None
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

class CelebVideoResponse(CelebVideoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CelebVideoList(BaseModel):
    items: list[CelebVideoResponse]
    total: int
    skip: int
    limit: int
