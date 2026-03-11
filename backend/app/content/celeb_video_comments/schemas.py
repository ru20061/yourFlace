from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class CelebVideoCommentBase(BaseModel):
    celeb_video_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str
    commenter_role: Literal["fan", "celeb", "manager"]
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class CelebVideoCommentCreate(CelebVideoCommentBase):
    pass

class CelebVideoCommentUpdate(BaseModel):
    celeb_video_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    content: Optional[str] = None
    commenter_role: Optional[Literal["fan", "celeb", "manager"]] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class CelebVideoCommentResponse(CelebVideoCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CelebVideoCommentList(BaseModel):
    items: list[CelebVideoCommentResponse]
    total: int
    skip: int
    limit: int
