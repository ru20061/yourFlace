from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistImageStatBase(BaseModel):
    pass

class ArtistImageStatCreate(ArtistImageStatBase):
    pass

class ArtistImageStatUpdate(BaseModel):
    pass

class ArtistImageStatResponse(ArtistImageStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistImageStatList(BaseModel):
    items: list[ArtistImageStatResponse]
    total: int
    skip: int
    limit: int
