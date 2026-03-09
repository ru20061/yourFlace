from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreatorCategoryMapBase(BaseModel):
    creator_id: int
    category_id: int

class CreatorCategoryMapCreate(CreatorCategoryMapBase):
    pass

class CreatorCategoryMapUpdate(BaseModel):
    pass

class CreatorCategoryMapResponse(CreatorCategoryMapBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class CreatorCategoryMapList(BaseModel):
    items: list[CreatorCategoryMapResponse]
    total: int
    skip: int
    limit: int
