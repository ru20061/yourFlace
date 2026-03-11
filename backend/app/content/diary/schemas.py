from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class DiaryBase(BaseModel):
    user_id: int
    celeb_id: int
    entry_date: date
    content_html: str


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(BaseModel):
    content_html: Optional[str] = None


class DiaryUpsert(BaseModel):
    """날짜별 저장/수정 — 프론트에서 단일 호출로 upsert"""
    user_id: int
    celeb_id: int
    entry_date: date
    content_html: str


class DiaryResponse(DiaryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class DiaryList(BaseModel):
    items: list[DiaryResponse]
    total: int
    skip: int
    limit: int
