from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistVideoBase(BaseModel):
    pass

class ArtistVideoCreate(ArtistVideoBase):
    pass

class ArtistVideoUpdate(BaseModel):
    pass

class ArtistVideoResponse(ArtistVideoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistVideoList(BaseModel):
    items: list[ArtistVideoResponse]
    total: int
    skip: int
    limit: int
