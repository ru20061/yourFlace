from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CelebCategoryMapBase(BaseModel):
    celeb_id: int
    category_id: int

class CelebCategoryMapCreate(CelebCategoryMapBase):
    pass

class CelebCategoryMapUpdate(BaseModel):
    pass

class CelebCategoryMapResponse(CelebCategoryMapBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class CelebCategoryMapList(BaseModel):
    items: list[CelebCategoryMapResponse]
    total: int
    skip: int
    limit: int
