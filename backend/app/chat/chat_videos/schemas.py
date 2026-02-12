from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatVideoBase(BaseModel):
    pass

class ChatVideoCreate(ChatVideoBase):
    pass

class ChatVideoUpdate(BaseModel):
    pass

class ChatVideoResponse(ChatVideoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatVideoList(BaseModel):
    items: list[ChatVideoResponse]
    total: int
    skip: int
    limit: int
