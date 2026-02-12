from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FanLikeBase(BaseModel):
    subscription_id: int
    target_type: str
    target_id: int

class FanLikeCreate(FanLikeBase):
    pass

class FanLikeUpdate(BaseModel):
    pass

class FanLikeResponse(FanLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class FanLikeList(BaseModel):
    items: list[FanLikeResponse]
    total: int
    skip: int
    limit: int
