from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ImageBase(BaseModel):
    pass

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    pass

class ImageResponse(ImageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ImageList(BaseModel):
    items: list[ImageResponse]
    total: int
    skip: int
    limit: int
