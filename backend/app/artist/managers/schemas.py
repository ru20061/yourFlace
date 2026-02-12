from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ManagerBase(BaseModel):
    pass

class ManagerCreate(ManagerBase):
    pass

class ManagerUpdate(BaseModel):
    pass

class ManagerResponse(ManagerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ManagerList(BaseModel):
    items: list[ManagerResponse]
    total: int
    skip: int
    limit: int
