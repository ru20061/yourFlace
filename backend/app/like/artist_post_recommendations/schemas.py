from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistPostRecommendationBase(BaseModel):
    artist_id: int
    post_id: int

class ArtistPostRecommendationCreate(ArtistPostRecommendationBase):
    pass

class ArtistPostRecommendationUpdate(BaseModel):
    pass

class ArtistPostRecommendationResponse(ArtistPostRecommendationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class ArtistPostRecommendationList(BaseModel):
    items: list[ArtistPostRecommendationResponse]
    total: int
    skip: int
    limit: int
