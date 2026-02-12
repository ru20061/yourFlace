from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistBase(BaseModel):
    pass

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    pass

class ArtistResponse(ArtistBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistList(BaseModel):
    items: list[ArtistResponse]
    total: int
    skip: int
    limit: int
