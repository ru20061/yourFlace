from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class ProductBase(BaseModel):
    pass

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    pass

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ProductList(BaseModel):
    items: list[ProductResponse]
    total: int
    skip: int
    limit: int
