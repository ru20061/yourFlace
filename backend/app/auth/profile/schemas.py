from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime, date

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Literal["male", "female"]] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None

class ProfileCreate(ProfileBase):
    user_id: int

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Literal["male", "female"]] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None

class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ProfileList(BaseModel):
    items: list[ProfileResponse]
    total: int
    skip: int
    limit: int
