from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistCategoryBase(BaseModel):
    pass

class ArtistCategoryCreate(ArtistCategoryBase):
    pass

class ArtistCategoryUpdate(BaseModel):
    pass

class ArtistCategoryResponse(ArtistCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistCategoryList(BaseModel):
    items: list[ArtistCategoryResponse]
    total: int
    skip: int
    limit: int
