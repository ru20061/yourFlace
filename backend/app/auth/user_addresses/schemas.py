from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UserAddressBase(BaseModel):
    address_name: Optional[str] = None
    recipient_name: str
    recipient_phone: str
    postal_code: str
    base_address: str
    detail_address: Optional[str] = None
    is_default: bool = False
    memo: Optional[str] = None

class UserAddressCreate(UserAddressBase):
    user_id: int

class UserAddressUpdate(BaseModel):
    address_name: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_phone: Optional[str] = None
    postal_code: Optional[str] = None
    base_address: Optional[str] = None
    detail_address: Optional[str] = None
    is_default: Optional[bool] = None
    memo: Optional[str] = None

class UserAddressResponse(UserAddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class UserAddressList(BaseModel):
    items: list[UserAddressResponse]
    total: int
    skip: int
    limit: int
