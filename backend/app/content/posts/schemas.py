from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal, Any
from datetime import datetime, date

class PostBase(BaseModel):
    author_id: int
    author_type: Literal["fan", "artist"]
    content: Optional[str] = None
    write_id: int
    write_role: Literal["fan", "artist", "manager"]
    visibility: Optional[Literal["public", "subscribers", "private"]] = "public"
    is_visible: Optional[bool] = True
    is_artist_post: Optional[bool] = False
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    title_field: Optional[str] = None
    search_text: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    author_id: Optional[int] = None
    author_type: Optional[Literal["fan", "artist"]] = None
    content: Optional[str] = None
    write_id: Optional[int] = None
    write_role: Optional[Literal["fan", "artist", "manager"]] = None
    visibility: Optional[Literal["public", "subscribers", "private"]] = None
    is_visible: Optional[bool] = None
    is_artist_post: Optional[bool] = None
    published_date: Optional[date] = None
    tags: Optional[Any] = None
    title_field: Optional[str] = None
    search_text: Optional[str] = None

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class PostList(BaseModel):
    items: list[PostResponse]
    total: int
    skip: int
    limit: int
