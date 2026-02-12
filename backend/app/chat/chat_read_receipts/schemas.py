from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatReadReceiptBase(BaseModel):
    pass

class ChatReadReceiptCreate(ChatReadReceiptBase):
    pass

class ChatReadReceiptUpdate(BaseModel):
    pass

class ChatReadReceiptResponse(ChatReadReceiptBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatReadReceiptList(BaseModel):
    items: list[ChatReadReceiptResponse]
    total: int
    skip: int
    limit: int
