from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ArtistVideoCommentBase(BaseModel):
    artist_video_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str
    commenter_role: Literal["fan", "artist", "manager"]
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class ArtistVideoCommentCreate(ArtistVideoCommentBase):
    pass

class ArtistVideoCommentUpdate(BaseModel):
    artist_video_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    content: Optional[str] = None
    commenter_role: Optional[Literal["fan", "artist", "manager"]] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class ArtistVideoCommentResponse(ArtistVideoCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ArtistVideoCommentList(BaseModel):
    items: list[ArtistVideoCommentResponse]
    total: int
    skip: int
    limit: int
