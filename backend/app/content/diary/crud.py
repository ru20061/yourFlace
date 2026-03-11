from typing import Optional, List
from datetime import date, datetime

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base_crud import BaseCRUD
from app.content.diary.models import Diary
from app.content.diary.schemas import DiaryCreate, DiaryUpdate


class CRUDDiary(BaseCRUD[Diary, DiaryCreate, DiaryUpdate]):

    async def get_by_date(
        self,
        db: AsyncSession,
        user_id: int,
        celeb_id: int,
        entry_date: date,
    ) -> Optional[Diary]:
        """유저 + 셀럽 + 날짜로 단건 조회"""
        stmt = select(Diary).where(
            and_(
                Diary.user_id == user_id,
                Diary.celeb_id == celeb_id,
                Diary.entry_date == entry_date,
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_celeb(
        self,
        db: AsyncSession,
        user_id: int,
        celeb_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Diary]:
        """유저 + 셀럽 기준 목록 조회 (날짜 범위 필터 선택)"""
        stmt = select(Diary).where(
            and_(
                Diary.user_id == user_id,
                Diary.celeb_id == celeb_id,
            )
        )
        if start_date:
            stmt = stmt.where(Diary.entry_date >= start_date)
        if end_date:
            stmt = stmt.where(Diary.entry_date <= end_date)
        stmt = stmt.order_by(Diary.entry_date.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def count_by_user_celeb(
        self,
        db: AsyncSession,
        user_id: int,
        celeb_id: int,
    ) -> int:
        from sqlalchemy import func
        stmt = select(func.count()).select_from(Diary).where(
            and_(
                Diary.user_id == user_id,
                Diary.celeb_id == celeb_id,
            )
        )
        result = await db.execute(stmt)
        return result.scalar()

    async def upsert(
        self,
        db: AsyncSession,
        user_id: int,
        celeb_id: int,
        entry_date: date,
        content_html: str,
    ) -> Diary:
        """날짜별 일기 저장 — 없으면 생성, 있으면 수정"""
        existing = await self.get_by_date(db, user_id, celeb_id, entry_date)
        if existing:
            stmt = (
                update(Diary)
                .where(Diary.id == existing.id)
                .values(content_html=content_html, updated_at=datetime.utcnow())
            )
            await db.execute(stmt)
            await db.flush()
            await db.refresh(existing)
            return existing
        else:
            db_obj = Diary(
                user_id=user_id,
                celeb_id=celeb_id,
                entry_date=entry_date,
                content_html=content_html,
            )
            db.add(db_obj)
            await db.flush()
            await db.refresh(db_obj)
            return db_obj

    async def delete_by_date(
        self,
        db: AsyncSession,
        user_id: int,
        celeb_id: int,
        entry_date: date,
    ) -> bool:
        """날짜별 일기 삭제"""
        existing = await self.get_by_date(db, user_id, celeb_id, entry_date)
        if not existing:
            return False
        await db.delete(existing)
        await db.flush()
        return True


diary_crud = CRUDDiary(Diary)
