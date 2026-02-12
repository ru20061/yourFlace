from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class SavedSearchFilterBase(BaseModel):
    user_id: int
    filter_name: str
    filter_data: dict[str, Any]
    is_default: Optional[bool] = False

class SavedSearchFilterCreate(SavedSearchFilterBase):
    pass

class SavedSearchFilterUpdate(BaseModel):
    filter_name: Optional[str] = None
    filter_data: Optional[dict[str, Any]] = None
    is_default: Optional[bool] = None

class SavedSearchFilterResponse(SavedSearchFilterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class SavedSearchFilterList(BaseModel):
    items: list[SavedSearchFilterResponse]
    total: int
    skip: int
    limit: int
