from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class UserSettingBase(BaseModel):
    language: str = "ko"
    theme: Literal["light", "dark"] = "light"
    show_profile: bool = True
    show_birth_date: bool = False
    show_activity_status: bool = True
    receive_system_notice: bool = True
    receive_system_app: bool = True
    receive_system_push: bool = True
    receive_system_email: bool = True

class UserSettingCreate(UserSettingBase):
    user_id: int

class UserSettingUpdate(BaseModel):
    language: Optional[str] = None
    theme: Optional[Literal["light", "dark"]] = None
    show_profile: Optional[bool] = None
    show_birth_date: Optional[bool] = None
    show_activity_status: Optional[bool] = None
    receive_system_notice: Optional[bool] = None
    receive_system_app: Optional[bool] = None
    receive_system_push: Optional[bool] = None
    receive_system_email: Optional[bool] = None

class UserSettingResponse(UserSettingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class UserSettingList(BaseModel):
    items: list[UserSettingResponse]
    total: int
    skip: int
    limit: int
