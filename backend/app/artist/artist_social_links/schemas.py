from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistSocialLinkBase(BaseModel):
    pass

class ArtistSocialLinkCreate(ArtistSocialLinkBase):
    pass

class ArtistSocialLinkUpdate(BaseModel):
    pass

class ArtistSocialLinkResponse(ArtistSocialLinkBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistSocialLinkList(BaseModel):
    items: list[ArtistSocialLinkResponse]
    total: int
    skip: int
    limit: int
