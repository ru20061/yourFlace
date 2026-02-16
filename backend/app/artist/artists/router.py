from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.artist.artists import crud, schemas
from app.artist.artists.models import Artist
from app.core.slug import generate_slug
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artists(
    obj_in: schemas.ArtistCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.artist_crud.create(db, obj_in)
    # slug 자동 생성
    if not obj.slug:
        base_slug = generate_slug(obj.stage_name)
        result = await db.execute(
            select(Artist.slug).where(Artist.slug.like(f"{base_slug}%"))
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

@router.get("/by-slug/{slug}", response_model=schemas.ArtistResponse)
async def get_artist_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """slug로 단건 조회"""
    result = await db.execute(
        select(Artist).where(Artist.slug == slug, Artist.status != "D")
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    return obj

@router.get("/{id}", response_model=schemas.ArtistResponse)
async def get_artists(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """단건 조회"""
    obj = await crud.artist_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    return obj

@router.get("", response_model=schemas.ArtistList)
async def get_artists_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """목록 조회"""
    items = await crud.artist_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.artist_crud.count(db)

    return schemas.ArtistList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.ArtistResponse)
async def update_artists(
    id: int,
    obj_in: schemas.ArtistUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.artist_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    # stage_name 변경 시 slug 재생성
    if obj_in.stage_name and obj_in.stage_name != obj.stage_name:
        base_slug = generate_slug(obj_in.stage_name)
        result = await db.execute(
            select(Artist.slug).where(Artist.slug.like(f"{base_slug}%"), Artist.id != id)
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
async def delete_artists(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.artist_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
