from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class SubscriptionBlacklistBase(BaseModel):
    actor_id: int
    actor_role: Literal["artist", "manager"]
    target_user_id: int
    reason: Optional[str] = None
    status: str = "active"

class SubscriptionBlacklistCreate(SubscriptionBlacklistBase):
    pass

class SubscriptionBlacklistUpdate(BaseModel):
    reason: Optional[str] = None
    status: Optional[str] = None

class SubscriptionBlacklistResponse(SubscriptionBlacklistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class SubscriptionBlacklistList(BaseModel):
    items: list[SubscriptionBlacklistResponse]
    total: int
    skip: int
    limit: int
