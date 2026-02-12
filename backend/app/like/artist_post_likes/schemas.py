from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistPostLikeBase(BaseModel):
    pass

class ArtistPostLikeCreate(ArtistPostLikeBase):
    pass

class ArtistPostLikeUpdate(BaseModel):
    pass

class ArtistPostLikeResponse(ArtistPostLikeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistPostLikeList(BaseModel):
    items: list[ArtistPostLikeResponse]
    total: int
    skip: int
    limit: int
