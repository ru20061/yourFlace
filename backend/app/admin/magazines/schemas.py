from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MagazineBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: Optional[str] = None
    artist_id: Optional[int] = None
    write_id: int
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = True

class MagazineCreate(MagazineBase):
    pass

class MagazineUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: Optional[str] = None
    artist_id: Optional[int] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None

class MagazineResponse(MagazineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    view_count: int
    created_at: datetime
    updated_at: datetime

class MagazineImageItem(BaseModel):
    id: int
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int = 0

class MagazineDetailResponse(MagazineResponse):
    images: list[MagazineImageItem] = []

class MagazineList(BaseModel):
    items: list[MagazineResponse]
    total: int
    skip: int
    limit: int
