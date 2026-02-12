from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ChatVideoBase(BaseModel):
    chat_message_id: int
    url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None

class ChatVideoCreate(ChatVideoBase):
    pass

class ChatVideoUpdate(BaseModel):
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None

class ChatVideoResponse(ChatVideoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class ChatVideoList(BaseModel):
    items: list[ChatVideoResponse]
    total: int
    skip: int
    limit: int
