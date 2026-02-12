from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatMessageBase(BaseModel):
    pass

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    pass

class ChatMessageResponse(ChatMessageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatMessageList(BaseModel):
    items: list[ChatMessageResponse]
    total: int
    skip: int
    limit: int
