from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorSocialLinkBase(BaseModel):
    platform_name: str
    url: str
    display_name: Optional[str] = None
    follower_count: int = 0
    priority: int = 0
    is_active: bool = True

class CreatorSocialLinkCreate(CreatorSocialLinkBase):
    creator_id: int

class CreatorSocialLinkUpdate(BaseModel):
    platform_name: Optional[str] = None
    url: Optional[str] = None
    display_name: Optional[str] = None
    follower_count: Optional[int] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

class CreatorSocialLinkResponse(CreatorSocialLinkBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime

class CreatorSocialLinkList(BaseModel):
    items: list[CreatorSocialLinkResponse]
    total: int
    skip: int
    limit: int
