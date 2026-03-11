from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class CelebImageCommentBase(BaseModel):
    celeb_image_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str
    commenter_role: Literal["fan", "celeb", "manager"]
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class CelebImageCommentCreate(CelebImageCommentBase):
    pass

class CelebImageCommentUpdate(BaseModel):
    celeb_image_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    content: Optional[str] = None
    commenter_role: Optional[Literal["fan", "celeb", "manager"]] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class CelebImageCommentResponse(CelebImageCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CelebImageCommentList(BaseModel):
    items: list[CelebImageCommentResponse]
    total: int
    skip: int
    limit: int
