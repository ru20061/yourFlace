from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistChatStatBase(BaseModel):
    pass

class ArtistChatStatCreate(ArtistChatStatBase):
    pass

class ArtistChatStatUpdate(BaseModel):
    pass

class ArtistChatStatResponse(ArtistChatStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistChatStatList(BaseModel):
    items: list[ArtistChatStatResponse]
    total: int
    skip: int
    limit: int
