from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProductImageBase(BaseModel):
    product_id: int
    image_id: int
    is_primary: Optional[bool] = False
    sort_order: Optional[int] = 0

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageUpdate(BaseModel):
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = None

class ProductImageResponse(ProductImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class ProductImageList(BaseModel):
    items: list[ProductImageResponse]
    total: int
    skip: int
    limit: int
