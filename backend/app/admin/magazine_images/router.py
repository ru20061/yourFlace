from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.admin.magazine_images import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.MagazineImageResponse, status_code=status.HTTP_201_CREATED)
async def create_magazine_image(
    obj_in: schemas.MagazineImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """생성"""
    obj = await crud.magazine_image_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.MagazineImageResponse)
async def get_magazine_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """단건 조회"""
    obj = await crud.magazine_image_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MagazineImage not found",
        )
    return obj

@router.get("", response_model=schemas.MagazineImageList)
async def get_magazine_images_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """목록 조회"""
    items = await crud.magazine_image_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.magazine_image_crud.count(db)
    return schemas.MagazineImageList(items=items, total=total, skip=skip, limit=limit)

@router.patch("/{id}", response_model=schemas.MagazineImageResponse)
async def update_magazine_image(
    id: int,
    obj_in: schemas.MagazineImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """업데이트"""
    obj = await crud.magazine_image_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MagazineImage not found",
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_magazine_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """삭제"""
    obj = await crud.magazine_image_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MagazineImage not found",
        )
    from sqlalchemy import delete as sql_delete
    from app.admin.magazine_images.models import MagazineImage
    await db.execute(sql_delete(MagazineImage).where(MagazineImage.id == id))
    await db.flush()
