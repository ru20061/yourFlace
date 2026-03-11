from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.celeb.celeb_categories import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.CelebCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_celeb_categories(
    obj_in: schemas.CelebCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.celeb_category_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.CelebCategoryResponse)
async def get_celeb_categories(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """단건 조회"""
    obj = await crud.celeb_category_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebCategory not found"
        )
    return obj

@router.get("", response_model=schemas.CelebCategoryList)
async def get_celeb_categories_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """목록 조회"""
    items = await crud.celeb_category_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.celeb_category_crud.count(db)

    return schemas.CelebCategoryList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.CelebCategoryResponse)
async def update_celeb_categories(
    id: int,
    obj_in: schemas.CelebCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.celeb_category_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebCategory not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_celeb_categories(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.celeb_category_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebCategory not found"
        )
