from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistPostLikeBase(BaseModel):
    artist_id: int
    post_id: int

class ArtistPostLikeCreate(ArtistPostLikeBase):
    pass

class ArtistPostLikeUpdate(BaseModel):
    pass

class ArtistPostLikeResponse(ArtistPostLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class ArtistPostLikeList(BaseModel):
    items: list[ArtistPostLikeResponse]
    total: int
    skip: int
    limit: int
