from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ModerationModelBase(BaseModel):
    model_name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class ModerationModelCreate(ModerationModelBase):
    pass

class ModerationModelUpdate(BaseModel):
    model_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ModerationModelResponse(ModerationModelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class ModerationModelList(BaseModel):
    items: list[ModerationModelResponse]
    total: int
    skip: int
    limit: int
