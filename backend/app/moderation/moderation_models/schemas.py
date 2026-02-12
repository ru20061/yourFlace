from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ModerationModelBase(BaseModel):
    pass

class ModerationModelCreate(ModerationModelBase):
    pass

class ModerationModelUpdate(BaseModel):
    pass

class ModerationModelResponse(ModerationModelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ModerationModelList(BaseModel):
    items: list[ModerationModelResponse]
    total: int
    skip: int
    limit: int
