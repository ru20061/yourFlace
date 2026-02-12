from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class SavedSearchFilterBase(BaseModel):
    pass

class SavedSearchFilterCreate(SavedSearchFilterBase):
    pass

class SavedSearchFilterUpdate(BaseModel):
    pass

class SavedSearchFilterResponse(SavedSearchFilterBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class SavedSearchFilterList(BaseModel):
    items: list[SavedSearchFilterResponse]
    total: int
    skip: int
    limit: int
