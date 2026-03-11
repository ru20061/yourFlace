from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebPostLikeBase(BaseModel):
    celeb_id: int
    post_id: int

class CelebPostLikeCreate(CelebPostLikeBase):
    pass

class CelebPostLikeUpdate(BaseModel):
    pass

class CelebPostLikeResponse(CelebPostLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime

class CelebPostLikeList(BaseModel):
    items: list[CelebPostLikeResponse]
    total: int
    skip: int
    limit: int
