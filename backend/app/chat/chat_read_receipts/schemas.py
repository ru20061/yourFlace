from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatReadReceiptBase(BaseModel):
    chat_message_id: int
    user_id: int

class ChatReadReceiptCreate(ChatReadReceiptBase):
    pass

class ChatReadReceiptUpdate(BaseModel):
    pass

class ChatReadReceiptResponse(ChatReadReceiptBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    read_at: datetime

class ChatReadReceiptList(BaseModel):
    items: list[ChatReadReceiptResponse]
    total: int
    skip: int
    limit: int
