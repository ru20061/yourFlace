from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatRoomBase(BaseModel):
    pass

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoomUpdate(BaseModel):
    pass

class ChatRoomResponse(ChatRoomBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatRoomList(BaseModel):
    items: list[ChatRoomResponse]
    total: int
    skip: int
    limit: int
