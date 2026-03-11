from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.like.celeb_post_recommendations import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.CelebPostRecommendationResponse, status_code=status.HTTP_201_CREATED)
async def create_celeb_post_recommendations(
    obj_in: schemas.CelebPostRecommendationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.celeb_post_recommendation_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.CelebPostRecommendationResponse)
async def get_celeb_post_recommendations(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.celeb_post_recommendation_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebPostRecommendation not found"
        )
    return obj

@router.get("", response_model=schemas.CelebPostRecommendationList)
async def get_celeb_post_recommendations_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    items = await crud.celeb_post_recommendation_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.celeb_post_recommendation_crud.count(db)

    return schemas.CelebPostRecommendationList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.CelebPostRecommendationResponse)
async def update_celeb_post_recommendations(
    id: int,
    obj_in: schemas.CelebPostRecommendationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.celeb_post_recommendation_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebPostRecommendation not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_celeb_post_recommendations(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.celeb_post_recommendation_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CelebPostRecommendation not found"
        )
