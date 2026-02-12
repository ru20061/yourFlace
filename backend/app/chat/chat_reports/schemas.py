from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ChatReportBase(BaseModel):
    pass

class ChatReportCreate(ChatReportBase):
    pass

class ChatReportUpdate(BaseModel):
    pass

class ChatReportResponse(ChatReportBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ChatReportList(BaseModel):
    items: list[ChatReportResponse]
    total: int
    skip: int
    limit: int
