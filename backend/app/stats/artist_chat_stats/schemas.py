from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArtistChatStatBase(BaseModel):
    artist_id: int
    chat_subscriber_count: Optional[int] = 0
    chat_image_count: Optional[int] = 0
    chat_video_count: Optional[int] = 0
    chat_attendance_days: Optional[int] = 0

class ArtistChatStatCreate(ArtistChatStatBase):
    pass

class ArtistChatStatUpdate(BaseModel):
    chat_subscriber_count: Optional[int] = None
    chat_image_count: Optional[int] = None
    chat_video_count: Optional[int] = None
    chat_attendance_days: Optional[int] = None

class ArtistChatStatResponse(ArtistChatStatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime

class ArtistChatStatList(BaseModel):
    items: list[ArtistChatStatResponse]
    total: int
    skip: int
    limit: int
