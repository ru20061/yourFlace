from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FAQBase(BaseModel):
    category: Optional[str] = None
    question: str
    answer: str
    priority: Optional[int] = 0
    is_active: Optional[bool] = True
    write_id: int

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

class FAQResponse(FAQBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class FAQList(BaseModel):
    items: list[FAQResponse]
    total: int
    skip: int
    limit: int
