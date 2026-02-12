from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PostStatBase(BaseModel):
    pass

class PostStatCreate(PostStatBase):
    pass

class PostStatUpdate(BaseModel):
    pass

class PostStatResponse(PostStatBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PostStatList(BaseModel):
    items: list[PostStatResponse]
    total: int
    skip: int
    limit: int
