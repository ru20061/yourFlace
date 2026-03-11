from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class CelebImageBase(BaseModel):
    celeb_id: int
    image_id: int
    write_id: int
    write_role: Literal["celeb", "manager", "artist"]
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = "public"
    is_visible: Optional[bool] = True
    search_text: Optional[str] = None

class CelebImageCreate(CelebImageBase):
    pass

class CelebImageUpdate(BaseModel):
    celeb_id: Optional[int] = None
    image_id: Optional[int] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["celeb", "manager", "artist"]] = None
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = None
    is_visible: Optional[bool] = None
    search_text: Optional[str] = None

class CelebImageResponse(CelebImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CelebImageWithAuthor(CelebImageResponse):
    """셀럽 이미지 + 구독 닉네임"""
    author_name: Optional[str] = None
    author_profile_image: Optional[str] = None

class CelebImageListWithAuthor(BaseModel):
    items: list[CelebImageWithAuthor]
    total: int
    skip: int
    limit: int

class CelebImageList(BaseModel):
    items: list[CelebImageResponse]
    total: int
    skip: int
    limit: int
