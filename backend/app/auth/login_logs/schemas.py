from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class LoginLogBase(BaseModel):
    ip_address: str
    device_type: Optional[str] = None
    device_info: Optional[str] = None
    status: Literal["success", "failed", "blocked"]
    fail_reason: Optional[str] = None

class LoginLogCreate(LoginLogBase):
    user_id: Optional[int] = None

class LoginLogUpdate(BaseModel):
    pass

class LoginLogResponse(LoginLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    created_at: datetime

class LoginLogList(BaseModel):
    items: list[LoginLogResponse]
    total: int
    skip: int
    limit: int
