from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ProductImageBase(BaseModel):
    pass

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(BaseModel):
    pass

class ProductImageResponse(ProductImageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ProductImageList(BaseModel):
    items: list[ProductImageResponse]
    total: int
    skip: int
    limit: int
