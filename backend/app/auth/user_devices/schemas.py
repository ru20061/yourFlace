from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class UserDeviceBase(BaseModel):
    device_type: Literal["ios", "android", "web"]
    device_token: Optional[str] = None
    app_version: Optional[str] = None
    os_version: Optional[str] = None
    is_active: bool = True

class UserDeviceCreate(UserDeviceBase):
    user_id: int

class UserDeviceUpdate(BaseModel):
    device_token: Optional[str] = None
    app_version: Optional[str] = None
    os_version: Optional[str] = None
    is_active: Optional[bool] = None
    last_used_at: Optional[datetime] = None

class UserDeviceResponse(UserDeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class UserDeviceList(BaseModel):
    items: list[UserDeviceResponse]
    total: int
    skip: int
    limit: int
