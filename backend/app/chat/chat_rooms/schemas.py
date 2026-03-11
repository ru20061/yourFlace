from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ChatRoomBase(BaseModel):
    room_type: Literal["fan", "celeb", "group", "direct", "subscription"]
    celeb_id: Optional[int] = None
    room_name: Optional[str] = None
    room_image: Optional[str] = None
    status: Optional[Literal["active", "inactive", "archived"]] = "active"

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoomUpdate(BaseModel):
    room_type: Optional[Literal["fan", "celeb", "group", "direct", "subscription"]] = None
    celeb_id: Optional[int] = None
    room_name: Optional[str] = None
    room_image: Optional[str] = None
    last_message_at: Optional[datetime] = None
    status: Optional[Literal["active", "inactive", "archived"]] = None

class ChatRoomResponse(ChatRoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_message_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class ChatRoomList(BaseModel):
    items: list[ChatRoomResponse]
    total: int
    skip: int
    limit: int
