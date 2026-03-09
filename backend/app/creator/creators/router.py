from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.creator.creators import crud, schemas
from app.creator.creators.models import Creator
from app.core.slug import generate_slug
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.CreatorResponse, status_code=status.HTTP_201_CREATED)
async def create_creators(
    obj_in: schemas.CreatorCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.creator_crud.create(db, obj_in)
    # slug 자동 생성
    if not obj.slug:
        base_slug = generate_slug(obj.stage_name)
        result = await db.execute(
            select(Creator.slug).where(Creator.slug.like(f"{base_slug}%"))
        )
        existing = [r[0] for r in result.fetchall() if r[0]]
        slug = base_slug
        if slug in existing:
            counter = 2
            while f"{slug}-{counter}" in existing:
                counter += 1
            slug = f"{slug}-{counter}"
        obj.slug = slug
        await db.flush()
        await db.refresh(obj)
    return obj

@router.get("/by-slug/{slug}", response_model=schemas.CreatorResponse)
async def get_creator_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """slug로 단건 조회"""
    result = await db.execute(
        select(Creator).where(Creator.slug == slug, Creator.status != "D")
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found"
        )
    return obj

@router.get("/{id}", response_model=schemas.CreatorResponse)
async def get_creators(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """단건 조회"""
    obj = await crud.creator_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found"
        )
    return obj

@router.get("", response_model=schemas.CreatorList)
async def get_creators_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """목록 조회"""
    items = await crud.creator_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.creator_crud.count(db)

    return schemas.CreatorList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.CreatorResponse)
async def update_creators(
    id: int,
    obj_in: schemas.CreatorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.creator_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found"
        )
    # stage_name 변경 시 slug 재생성
    if obj_in.stage_name and obj_in.stage_name != obj.stage_name:
        base_slug = generate_slug(obj_in.stage_name)
        result = await db.execute(
            select(Creator.slug).where(Creator.slug.like(f"{base_slug}%"), Creator.id != id)
        )
        existing = [r[0] for r in result.fetchall() if r[0]]
        slug = base_slug
        if slug in existing:
            counter = 2
            while f"{slug}-{counter}" in existing:
                counter += 1
            slug = f"{slug}-{counter}"
        obj.slug = slug
        await db.flush()
        await db.refresh(obj)
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_creators(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.creator_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found"
        )
