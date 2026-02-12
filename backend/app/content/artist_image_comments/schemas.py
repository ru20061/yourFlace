from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistImageCommentBase(BaseModel):
    pass

class ArtistImageCommentCreate(ArtistImageCommentBase):
    pass

class ArtistImageCommentUpdate(BaseModel):
    pass

class ArtistImageCommentResponse(ArtistImageCommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistImageCommentList(BaseModel):
    items: list[ArtistImageCommentResponse]
    total: int
    skip: int
    limit: int
