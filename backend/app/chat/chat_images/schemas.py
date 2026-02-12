from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatImageBase(BaseModel):
    pass

class ChatImageCreate(ChatImageBase):
    pass

class ChatImageUpdate(BaseModel):
    pass

class ChatImageResponse(ChatImageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatImageList(BaseModel):
    items: list[ChatImageResponse]
    total: int
    skip: int
    limit: int
