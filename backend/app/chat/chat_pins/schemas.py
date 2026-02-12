from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatPinBase(BaseModel):
    pass

class ChatPinCreate(ChatPinBase):
    pass

class ChatPinUpdate(BaseModel):
    pass

class ChatPinResponse(ChatPinBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatPinList(BaseModel):
    items: list[ChatPinResponse]
    total: int
    skip: int
    limit: int
