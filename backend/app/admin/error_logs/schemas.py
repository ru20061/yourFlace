from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ErrorLogBase(BaseModel):
    error_type: str
    message: Optional[str] = None
    stack_trace: Optional[str] = None
    severity: Literal["info", "warning", "error", "critical", "low", "medium", "high"]
    source_module: Optional[str] = None
    user_id: Optional[int] = None
    resolved: Optional[bool] = False

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogUpdate(BaseModel):
    resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None

class ErrorLogResponse(ErrorLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resolved_at: Optional[datetime] = None
    created_at: datetime

class ErrorLogList(BaseModel):
    items: list[ErrorLogResponse]
    total: int
    skip: int
    limit: int
