from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MagazineImageBase(BaseModel):
    magazine_id: int
    image_id: int
    sort_order: Optional[int] = 0

class MagazineImageCreate(MagazineImageBase):
    pass

class MagazineImageUpdate(BaseModel):
    magazine_id: Optional[int] = None
    image_id: Optional[int] = None
    sort_order: Optional[int] = None

class MagazineImageResponse(MagazineImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class MagazineImageList(BaseModel):
    items: list[MagazineImageResponse]
    total: int
    skip: int
    limit: int
