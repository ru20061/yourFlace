from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistCategoryMapBase(BaseModel):
    pass

class ArtistCategoryMapCreate(ArtistCategoryMapBase):
    pass

class ArtistCategoryMapUpdate(BaseModel):
    pass

class ArtistCategoryMapResponse(ArtistCategoryMapBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistCategoryMapList(BaseModel):
    items: list[ArtistCategoryMapResponse]
    total: int
    skip: int
    limit: int
