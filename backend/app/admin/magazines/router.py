from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.admin.magazines import crud, schemas
from app.admin.magazines.models import Magazine
from app.admin.magazine_images.models import MagazineImage
from app.content.images.models import Image
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/public", response_model=schemas.MagazineList)
async def get_public_magazines(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """공개 매거진 목록 조회 (is_active=True, 인증 불필요)"""
    filters = {"is_active": True}
    items = await crud.magazine_crud.get_multi(db, skip=skip, limit=limit, filters=filters)
    total = await crud.magazine_crud.count(db, filters=filters)
    return schemas.MagazineList(items=items, total=total, skip=skip, limit=limit)

@router.get("/public/{id}", response_model=schemas.MagazineDetailResponse)
async def get_public_magazine_detail(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """공개 매거진 상세 조회 (이미지 포함, 인증 불필요)"""
    magazine = await crud.magazine_crud.get(db, id)
    if not magazine or not magazine.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Magazine not found")

    stmt = (
        select(MagazineImage.id, MagazineImage.sort_order, Image.url, Image.width, Image.height)
        .join(Image, MagazineImage.image_id == Image.id)
        .where(MagazineImage.magazine_id == id)
        .order_by(MagazineImage.sort_order)
    )
    result = await db.execute(stmt)
    images = [
        {"id": row.id, "url": row.url, "width": row.width, "height": row.height, "sort_order": row.sort_order}
        for row in result.fetchall()
    ]

    return schemas.MagazineDetailResponse(
        id=magazine.id,
        title=magazine.title,
        content=magazine.content,
        summary=magazine.summary,
        thumbnail_url=magazine.thumbnail_url,
        category=magazine.category,
        artist_id=magazine.artist_id,
        write_id=magazine.write_id,
        tags=magazine.tags,
        is_active=magazine.is_active,
        view_count=magazine.view_count,
        created_at=magazine.created_at,
        updated_at=magazine.updated_at,
        images=images,
    )

@router.post("", response_model=schemas.MagazineResponse, status_code=status.HTTP_201_CREATED)
async def create_magazine(
    obj_in: schemas.MagazineCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """생성"""
    obj = await crud.magazine_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.MagazineResponse)
async def get_magazine(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """단건 조회"""
    obj = await crud.magazine_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magazine not found",
        )
    return obj

@router.get("", response_model=schemas.MagazineList)
async def get_magazines_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """목록 조회"""
    items = await crud.magazine_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.magazine_crud.count(db)
    return schemas.MagazineList(items=items, total=total, skip=skip, limit=limit)

@router.patch("/{id}", response_model=schemas.MagazineResponse)
async def update_magazine(
    id: int,
    obj_in: schemas.MagazineUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """업데이트"""
    obj = await crud.magazine_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magazine not found",
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_magazine(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """삭제"""
    from sqlalchemy import update as sql_update, delete as sql_delete
    from app.admin.magazines.models import Magazine
    from datetime import datetime

    obj = await crud.magazine_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magazine not found",
        )
    stmt = sql_update(Magazine).where(Magazine.id == id).values(is_active=False, updated_at=datetime.utcnow())
    await db.execute(stmt)
    await db.flush()
