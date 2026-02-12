from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    status: Optional[str] = "active"

class UserCreate(UserBase):
    """관리자용 사용자 생성 (password_hash 직접 설정)"""
    password_hash: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None

class UserUpdate(BaseModel):
    """사용자 정보 수정"""
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None
    status: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None

class UserResponse(UserBase):
    """사용자 응답 스키마"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserList(BaseModel):
    """사용자 목록 응답"""
    items: list[UserResponse]
    total: int
    skip: int
    limit: int
