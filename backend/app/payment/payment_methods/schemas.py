from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class PaymentMethodBase(BaseModel):
    user_id: int
    method_type: str
    provider: Optional[str] = None
    account_info: Optional[dict[str, Any]] = None
    is_default: Optional[bool] = False
    is_active: Optional[bool] = True

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    method_type: Optional[str] = None
    provider: Optional[str] = None
    account_info: Optional[dict[str, Any]] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class PaymentMethodResponse(PaymentMethodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class PaymentMethodList(BaseModel):
    items: list[PaymentMethodResponse]
    total: int
    skip: int
    limit: int
