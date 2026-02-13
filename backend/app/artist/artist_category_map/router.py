from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.artist.artist_category_map import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.ArtistCategoryMapResponse, status_code=status.HTTP_201_CREATED)
async def create_artist_category_map(
    obj_in: schemas.ArtistCategoryMapCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.artist_category_map_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.ArtistCategoryMapResponse)
async def get_artist_category_map(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.artist_category_map_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistCategoryMap not found"
        )
    return obj

@router.get("", response_model=schemas.ArtistCategoryMapList)
async def get_artist_category_map_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    items = await crud.artist_category_map_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.artist_category_map_crud.count(db)
    
    return schemas.ArtistCategoryMapList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.ArtistCategoryMapResponse)
async def update_artist_category_map(
    id: int,
    obj_in: schemas.ArtistCategoryMapUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.artist_category_map_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistCategoryMap not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist_category_map(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.artist_category_map_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistCategoryMap not found"
        )
