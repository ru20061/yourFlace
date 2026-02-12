from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistImageBase(BaseModel):
    pass

class ArtistImageCreate(ArtistImageBase):
    pass

class ArtistImageUpdate(BaseModel):
    pass

class ArtistImageResponse(ArtistImageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistImageList(BaseModel):
    items: list[ArtistImageResponse]
    total: int
    skip: int
    limit: int
