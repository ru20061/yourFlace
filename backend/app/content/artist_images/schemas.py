from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class ArtistImageBase(BaseModel):
    artist_id: int
    image_id: int
    write_id: int
    write_role: Literal["artist", "manager"]
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = "public"
    is_visible: Optional[bool] = True
    search_text: Optional[str] = None

class ArtistImageCreate(ArtistImageBase):
    pass

class ArtistImageUpdate(BaseModel):
    artist_id: Optional[int] = None
    image_id: Optional[int] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["artist", "manager"]] = None
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = None
    is_visible: Optional[bool] = None
    search_text: Optional[str] = None

class ArtistImageResponse(ArtistImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ArtistImageWithAuthor(ArtistImageResponse):
    """아티스트 이미지 + 구독 닉네임"""
    author_name: Optional[str] = None
    author_profile_image: Optional[str] = None

class ArtistImageListWithAuthor(BaseModel):
    items: list[ArtistImageWithAuthor]
    total: int
    skip: int
    limit: int

class ArtistImageList(BaseModel):
    items: list[ArtistImageResponse]
    total: int
    skip: int
    limit: int
