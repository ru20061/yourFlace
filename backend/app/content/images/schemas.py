from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ImageBase(BaseModel):
    url: str
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None

class ImageResponse(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class ImageList(BaseModel):
    items: list[ImageResponse]
    total: int
    skip: int
    limit: int
