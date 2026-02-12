from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FanRecommendationBase(BaseModel):
    subscription_id: int
    target_type: str
    target_id: int

class FanRecommendationCreate(FanRecommendationBase):
    pass

class FanRecommendationUpdate(BaseModel):
    pass

class FanRecommendationResponse(FanRecommendationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class FanRecommendationList(BaseModel):
    items: list[FanRecommendationResponse]
    total: int
    skip: int
    limit: int
