from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class CreatorVideoCommentBase(BaseModel):
    creator_video_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str
    commenter_role: Literal["fan", "creator", "manager"]
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class CreatorVideoCommentCreate(CreatorVideoCommentBase):
    pass

class CreatorVideoCommentUpdate(BaseModel):
    creator_video_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    content: Optional[str] = None
    commenter_role: Optional[Literal["fan", "creator", "manager"]] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class CreatorVideoCommentResponse(CreatorVideoCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CreatorVideoCommentList(BaseModel):
    items: list[CreatorVideoCommentResponse]
    total: int
    skip: int
    limit: int
