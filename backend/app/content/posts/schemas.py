from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PostBase(BaseModel):
    pass

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PostList(BaseModel):
    items: list[PostResponse]
    total: int
    skip: int
    limit: int
