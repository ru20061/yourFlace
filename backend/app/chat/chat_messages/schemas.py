from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ChatMessageBase(BaseModel):
    chat_room_id: int
    sender_id: int
    sender_type: Literal["fan", "artist", "system"]
    message_type: Optional[Literal["text", "image", "video", "file"]] = "text"
    content: Optional[str] = None
    is_pinned: Optional[bool] = False
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    content: Optional[str] = None
    is_pinned: Optional[bool] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class ChatMessageResponse(ChatMessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ChatMessageList(BaseModel):
    items: list[ChatMessageResponse]
    total: int
    skip: int
    limit: int
