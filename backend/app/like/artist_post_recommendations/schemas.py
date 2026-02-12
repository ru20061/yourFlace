from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ArtistPostRecommendationBase(BaseModel):
    pass

class ArtistPostRecommendationCreate(ArtistPostRecommendationBase):
    pass

class ArtistPostRecommendationUpdate(BaseModel):
    pass

class ArtistPostRecommendationResponse(ArtistPostRecommendationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ArtistPostRecommendationList(BaseModel):
    items: list[ArtistPostRecommendationResponse]
    total: int
    skip: int
    limit: int
