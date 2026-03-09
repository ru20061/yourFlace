from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorChatStatBase(BaseModel):
    creator_id: int
    chat_subscriber_count: Optional[int] = 0
    chat_image_count: Optional[int] = 0
    chat_video_count: Optional[int] = 0
    chat_attendance_days: Optional[int] = 0

class CreatorChatStatCreate(CreatorChatStatBase):
    pass

class CreatorChatStatUpdate(BaseModel):
    chat_subscriber_count: Optional[int] = None
    chat_image_count: Optional[int] = None
    chat_video_count: Optional[int] = None
    chat_attendance_days: Optional[int] = None

class CreatorChatStatResponse(CreatorChatStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime

class CreatorChatStatList(BaseModel):
    items: list[CreatorChatStatResponse]
    total: int
    skip: int
    limit: int
