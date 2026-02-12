from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistVideoStatBase(BaseModel):
    pass

class ArtistVideoStatCreate(ArtistVideoStatBase):
    pass

class ArtistVideoStatUpdate(BaseModel):
    pass

class ArtistVideoStatResponse(ArtistVideoStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistVideoStatList(BaseModel):
    items: list[ArtistVideoStatResponse]
    total: int
    skip: int
    limit: int
