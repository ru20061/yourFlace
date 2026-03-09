from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.creator.creator_categories import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.CreatorCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_creator_categories(
    obj_in: schemas.CreatorCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.creator_category_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.CreatorCategoryResponse)
async def get_creator_categories(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """단건 조회"""
    obj = await crud.creator_category_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CreatorCategory not found"
        )
    return obj

@router.get("", response_model=schemas.CreatorCategoryList)
async def get_creator_categories_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """목록 조회"""
    items = await crud.creator_category_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.creator_category_crud.count(db)

    return schemas.CreatorCategoryList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.CreatorCategoryResponse)
async def update_creator_categories(
    id: int,
    obj_in: schemas.CreatorCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.creator_category_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CreatorCategory not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_creator_categories(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.creator_category_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CreatorCategory not found"
        )
