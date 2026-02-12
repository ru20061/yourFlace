from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistContentStatBase(BaseModel):
    pass

class ArtistContentStatCreate(ArtistContentStatBase):
    pass

class ArtistContentStatUpdate(BaseModel):
    pass

class ArtistContentStatResponse(ArtistContentStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistContentStatList(BaseModel):
    items: list[ArtistContentStatResponse]
    total: int
    skip: int
    limit: int
