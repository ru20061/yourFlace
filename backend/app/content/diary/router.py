from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.content.diary import schemas
from app.content.diary.crud import diary_crud

router = APIRouter()


@router.put("/upsert", response_model=schemas.DiaryResponse)
async def upsert_diary(
    obj_in: schemas.DiaryUpsert,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """날짜별 일기 저장 — 없으면 생성, 있으면 수정 (프론트 메인 저장 API)"""
    if current_user.id != obj_in.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 저장할 수 있습니다.")
    return await diary_crud.upsert(
        db,
        user_id=obj_in.user_id,
        celeb_id=obj_in.celeb_id,
        entry_date=obj_in.entry_date,
        content_html=obj_in.content_html,
    )


@router.get("", response_model=schemas.DiaryList)
async def get_diary_list(
    user_id: int = Query(...),
    celeb_id: int = Query(...),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """유저 + 셀럽 기준 일기 목록 조회"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 조회할 수 있습니다.")
    items = await diary_crud.get_by_user_celeb(
        db,
        user_id=user_id,
        celeb_id=celeb_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    total = await diary_crud.count_by_user_celeb(db, user_id=user_id, celeb_id=celeb_id)
    return schemas.DiaryList(items=items, total=total, skip=skip, limit=limit)


@router.get("/by-date", response_model=schemas.DiaryResponse)
async def get_diary_by_date(
    user_id: int = Query(...),
    celeb_id: int = Query(...),
    entry_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """특정 날짜 일기 단건 조회"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 조회할 수 있습니다.")
    obj = await diary_crud.get_by_date(db, user_id=user_id, celeb_id=celeb_id, entry_date=entry_date)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 날짜의 일기가 없습니다.")
    return obj


@router.get("/{id}", response_model=schemas.DiaryResponse)
async def get_diary(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """ID로 단건 조회"""
    obj = await diary_crud.get(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")
    if current_user.id != obj.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 조회할 수 있습니다.")
    return obj


@router.patch("/{id}", response_model=schemas.DiaryResponse)
async def update_diary(
    id: int,
    obj_in: schemas.DiaryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """내용 수정"""
    obj = await diary_crud.get(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")
    if current_user.id != obj.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 수정할 수 있습니다.")
    updated = await diary_crud.update(db, id, obj_in)
    return updated


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary_by_date(
    user_id: int = Query(...),
    celeb_id: int = Query(...),
    entry_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """날짜로 일기 삭제"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 삭제할 수 있습니다.")
    success = await diary_crud.delete_by_date(
        db, user_id=user_id, celeb_id=celeb_id, entry_date=entry_date
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 날짜의 일기가 없습니다.")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """ID로 일기 삭제"""
    obj = await diary_crud.get(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")
    if current_user.id != obj.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="본인의 일기만 삭제할 수 있습니다.")
    await db.delete(obj)
    await db.flush()
