from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CelebCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CelebCategoryCreate(CelebCategoryBase):
    pass

class CelebCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CelebCategoryResponse(CelebCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CelebCategoryList(BaseModel):
    items: list[CelebCategoryResponse]
    total: int
    skip: int
    limit: int
