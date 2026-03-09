from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class CreatorImageCommentBase(BaseModel):
    creator_image_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str
    commenter_role: Literal["fan", "creator", "manager"]
    status: Optional[Literal["active", "deleted", "reported"]] = "active"

class CreatorImageCommentCreate(CreatorImageCommentBase):
    pass

class CreatorImageCommentUpdate(BaseModel):
    creator_image_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_comment_id: Optional[int] = None
    content: Optional[str] = None
    commenter_role: Optional[Literal["fan", "creator", "manager"]] = None
    status: Optional[Literal["active", "deleted", "reported"]] = None

class CreatorImageCommentResponse(CreatorImageCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CreatorImageCommentList(BaseModel):
    items: list[CreatorImageCommentResponse]
    total: int
    skip: int
    limit: int
