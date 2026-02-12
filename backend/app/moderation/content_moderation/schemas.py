from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class ContentModerationBase(BaseModel):
    content_type: str
    content_id: int
    creator_ref_type: Optional[str] = None
    creator_ref_id: Optional[int] = None
    model_id: Optional[int] = None
    result: Optional[dict[str, Any]] = None
    is_flagged: Optional[bool] = False
    flagged_reason: Optional[str] = None
    reviewed: Optional[bool] = False
    reviewed_by: Optional[int] = None

class ContentModerationCreate(ContentModerationBase):
    pass

class ContentModerationUpdate(BaseModel):
    result: Optional[dict[str, Any]] = None
    is_flagged: Optional[bool] = None
    flagged_reason: Optional[str] = None
    reviewed: Optional[bool] = None
    reviewed_by: Optional[int] = None

class ContentModerationResponse(ContentModerationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ContentModerationList(BaseModel):
    items: list[ContentModerationResponse]
    total: int
    skip: int
    limit: int
