from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ArtistCategoryMapBase(BaseModel):
    artist_id: int
    category_id: int

class ArtistCategoryMapCreate(ArtistCategoryMapBase):
    pass

class ArtistCategoryMapUpdate(BaseModel):
    pass

class ArtistCategoryMapResponse(ArtistCategoryMapBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class ArtistCategoryMapList(BaseModel):
    items: list[ArtistCategoryMapResponse]
    total: int
    skip: int
    limit: int
