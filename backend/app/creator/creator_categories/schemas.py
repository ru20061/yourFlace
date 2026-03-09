from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreatorCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CreatorCategoryCreate(CreatorCategoryBase):
    pass

class CreatorCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CreatorCategoryResponse(CreatorCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CreatorCategoryList(BaseModel):
    items: list[CreatorCategoryResponse]
    total: int
    skip: int
    limit: int
