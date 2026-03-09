from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorPostRecommendationBase(BaseModel):
    creator_id: int
    post_id: int

class CreatorPostRecommendationCreate(CreatorPostRecommendationBase):
    pass

class CreatorPostRecommendationUpdate(BaseModel):
    pass

class CreatorPostRecommendationResponse(CreatorPostRecommendationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class CreatorPostRecommendationList(BaseModel):
    items: list[CreatorPostRecommendationResponse]
    total: int
    skip: int
    limit: int
