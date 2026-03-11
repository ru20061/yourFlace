from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebPostRecommendationBase(BaseModel):
    celeb_id: int
    post_id: int

class CelebPostRecommendationCreate(CelebPostRecommendationBase):
    pass

class CelebPostRecommendationUpdate(BaseModel):
    pass

class CelebPostRecommendationResponse(CelebPostRecommendationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class CelebPostRecommendationList(BaseModel):
    items: list[CelebPostRecommendationResponse]
    total: int
    skip: int
    limit: int
