from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorPostLikeBase(BaseModel):
    creator_id: int
    post_id: int

class CreatorPostLikeCreate(CreatorPostLikeBase):
    pass

class CreatorPostLikeUpdate(BaseModel):
    pass

class CreatorPostLikeResponse(CreatorPostLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class CreatorPostLikeList(BaseModel):
    items: list[CreatorPostLikeResponse]
    total: int
    skip: int
    limit: int
