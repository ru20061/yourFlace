from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PostImageBase(BaseModel):
    pass

class PostImageCreate(PostImageBase):
    pass

class PostImageUpdate(BaseModel):
    pass

class PostImageResponse(PostImageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PostImageList(BaseModel):
    items: list[PostImageResponse]
    total: int
    skip: int
    limit: int
