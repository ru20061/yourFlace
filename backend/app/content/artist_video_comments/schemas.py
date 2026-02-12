from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistVideoCommentBase(BaseModel):
    pass

class ArtistVideoCommentCreate(ArtistVideoCommentBase):
    pass

class ArtistVideoCommentUpdate(BaseModel):
    pass

class ArtistVideoCommentResponse(ArtistVideoCommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistVideoCommentList(BaseModel):
    items: list[ArtistVideoCommentResponse]
    total: int
    skip: int
    limit: int
