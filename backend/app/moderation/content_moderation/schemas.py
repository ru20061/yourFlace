from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ContentModerationBase(BaseModel):
    pass

class ContentModerationCreate(ContentModerationBase):
    pass

class ContentModerationUpdate(BaseModel):
    pass

class ContentModerationResponse(ContentModerationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ContentModerationList(BaseModel):
    items: list[ContentModerationResponse]
    total: int
    skip: int
    limit: int
