from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.subscription.subscriptions import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscriptions(
    obj_in: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.subscription_crud.create(db, obj_in)
    return obj

@router.get("/check", response_model=None)
async def check_subscription(
    fan_id: int = Query(...),
    celeb_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """그룹 구독 포함 구독 여부 확인 (개인 멤버는 소속 그룹 구독도 인정)"""
    subscribed = await crud.subscription_crud.is_subscribed(db, fan_id=fan_id, celeb_id=celeb_id)
    return {"is_subscribed": subscribed}


@router.get("/{id}", response_model=schemas.SubscriptionResponse)
async def get_subscriptions(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.subscription_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return obj

@router.get("", response_model=schemas.SubscriptionList)
async def get_subscriptions_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    fan_id: Optional[int] = Query(None),
    celeb_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    filters = {}
    if fan_id is not None:
        filters["fan_id"] = fan_id
    if celeb_id is not None:
        filters["celeb_id"] = celeb_id

    items = await crud.subscription_crud.get_multi(db, skip=skip, limit=limit, filters=filters or None)
    total = await crud.subscription_crud.count(db, filters=filters or None)

    return schemas.SubscriptionList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.SubscriptionResponse)
async def update_subscriptions(
    id: int,
    obj_in: schemas.SubscriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.subscription_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscriptions(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.subscription_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
