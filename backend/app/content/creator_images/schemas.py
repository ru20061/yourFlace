from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class CreatorImageBase(BaseModel):
    creator_id: int
    image_id: int
    write_id: int
    write_role: Literal["creator", "manager"]
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = "public"
    is_visible: Optional[bool] = True
    search_text: Optional[str] = None

class CreatorImageCreate(CreatorImageBase):
    pass

class CreatorImageUpdate(BaseModel):
    creator_id: Optional[int] = None
    image_id: Optional[int] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["creator", "manager"]] = None
    image_purpose: Optional[str] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = None
    is_visible: Optional[bool] = None
    search_text: Optional[str] = None

class CreatorImageResponse(CreatorImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CreatorImageWithAuthor(CreatorImageResponse):
    """크리에이터 이미지 + 구독 닉네임"""
    author_name: Optional[str] = None
    author_profile_image: Optional[str] = None

class CreatorImageListWithAuthor(BaseModel):
    items: list[CreatorImageWithAuthor]
    total: int
    skip: int
    limit: int

class CreatorImageList(BaseModel):
    items: list[CreatorImageResponse]
    total: int
    skip: int
    limit: int
