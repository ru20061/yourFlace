from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class ArtistBase(BaseModel):
    stage_name: str
    notes: Optional[str] = None
    profile_image: Optional[str] = None
    cover_image: Optional[str] = None
    status: Literal["active", "inactive"] = "active"

class ArtistCreate(ArtistBase):
    user_id: int

class ArtistUpdate(BaseModel):
    stage_name: Optional[str] = None
    notes: Optional[str] = None
    profile_image: Optional[str] = None
    cover_image: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None

class ArtistResponse(ArtistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    slug: Optional[str] = None
    search_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ArtistList(BaseModel):
    items: list[ArtistResponse]
    total: int
    skip: int
    limit: int
