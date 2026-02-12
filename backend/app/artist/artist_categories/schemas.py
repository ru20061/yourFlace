from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class ArtistCategoryCreate(ArtistCategoryBase):
    pass

class ArtistCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ArtistCategoryResponse(ArtistCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ArtistCategoryList(BaseModel):
    items: list[ArtistCategoryResponse]
    total: int
    skip: int
    limit: int
