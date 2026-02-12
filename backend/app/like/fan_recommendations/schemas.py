from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class FanRecommendationBase(BaseModel):
    pass

class FanRecommendationCreate(FanRecommendationBase):
    pass

class FanRecommendationUpdate(BaseModel):
    pass

class FanRecommendationResponse(FanRecommendationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class FanRecommendationList(BaseModel):
    items: list[FanRecommendationResponse]
    total: int
    skip: int
    limit: int
