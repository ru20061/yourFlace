from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class PostCommentBase(BaseModel):
    pass

class PostCommentCreate(PostCommentBase):
    pass

class PostCommentUpdate(BaseModel):
    pass

class PostCommentResponse(PostCommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class PostCommentList(BaseModel):
    items: list[PostCommentResponse]
    total: int
    skip: int
    limit: int
