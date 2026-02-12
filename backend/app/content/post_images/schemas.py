from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PostImageBase(BaseModel):
    post_id: int
    image_id: int
    sort_order: Optional[int] = 0

class PostImageCreate(PostImageBase):
    pass

class PostImageUpdate(BaseModel):
    post_id: Optional[int] = None
    image_id: Optional[int] = None
    sort_order: Optional[int] = None

class PostImageResponse(PostImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class PostImageList(BaseModel):
    items: list[PostImageResponse]
    total: int
    skip: int
    limit: int
