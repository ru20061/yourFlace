from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatImageBase(BaseModel):
    chat_message_id: int
    image_id: int

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
