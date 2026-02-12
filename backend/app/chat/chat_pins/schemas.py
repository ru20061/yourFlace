from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatPinBase(BaseModel):
    chat_room_id: int
    chat_message_id: int
    pinned_by: int

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
