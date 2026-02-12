from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class BannerBase(BaseModel):
    pass

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    pass

class BannerResponse(BannerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class BannerList(BaseModel):
    items: list[BannerResponse]
    total: int
    skip: int
    limit: int
