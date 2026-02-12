from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BannerBase(BaseModel):
    position: str
    title: Optional[str] = None
    image_url: str
    link_url: Optional[str] = None
    priority: Optional[int] = 0
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    write_id: int

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    position: Optional[str] = None
    title: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    priority: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class BannerResponse(BannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class BannerList(BaseModel):
    items: list[BannerResponse]
    total: int
    skip: int
    limit: int
