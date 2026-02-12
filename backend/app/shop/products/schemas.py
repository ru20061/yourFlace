from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    artist_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    currency: Optional[str] = "KRW"
    stock: Optional[int] = 0
    category: Optional[str] = None
    sale_start: Optional[datetime] = None
    sale_end: Optional[datetime] = None
    status: Optional[Literal["active", "inactive", "sold_out", "discontinued"]] = "active"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    sale_start: Optional[datetime] = None
    sale_end: Optional[datetime] = None
    status: Optional[Literal["active", "inactive", "sold_out", "discontinued"]] = None

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ProductList(BaseModel):
    items: list[ProductResponse]
    total: int
    skip: int
    limit: int
