from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sa_update, and_, select, func, desc
from app.database import get_db
from app.auth.user_addresses import crud, schemas
from app.auth.user_addresses.models import UserAddress
from app.dependencies import get_current_user

router = APIRouter()


async def _clear_default(db: AsyncSession, user_id: int, exclude_id: int | None = None):
    """해당 사용자의 다른 기본 배송지를 모두 해제"""
    conditions = [UserAddress.user_id == user_id, UserAddress.is_default == True]
    if exclude_id:
        conditions.append(UserAddress.id != exclude_id)
    stmt = sa_update(UserAddress).where(and_(*conditions)).values(is_default=False)
    await db.execute(stmt)

@router.post("", response_model=schemas.UserAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_user_addresses(
    obj_in: schemas.UserAddressCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성 - 현재 로그인한 사용자의 배송지 추가"""
    obj_in.user_id = current_user.id
    if obj_in.is_default:
        await _clear_default(db, current_user.id)
    obj = await crud.user_address_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.UserAddressResponse)
async def get_user_addresses(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회 - 본인 배송지만 조회 가능"""
    obj = await crud.user_address_crud.get(db, id)
    if not obj or obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAddress not found"
        )
    return obj

@router.get("", response_model=schemas.UserAddressList)
async def get_user_addresses_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회 - 현재 로그인한 사용자의 배송지만 반환 (기본배송지 우선)"""
    base_filter = and_(
        UserAddress.user_id == current_user.id,
        UserAddress.status != 'D'
    )
    stmt = (
        select(UserAddress)
        .where(base_filter)
        .order_by(desc(UserAddress.is_default), UserAddress.created_at)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    count_stmt = select(func.count()).select_from(UserAddress).where(base_filter)
    total = (await db.execute(count_stmt)).scalar()

    return schemas.UserAddressList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.UserAddressResponse)
async def update_user_addresses(
    id: int,
    obj_in: schemas.UserAddressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트 - 본인 배송지만 수정 가능"""
    existing = await crud.user_address_crud.get(db, id)
    if not existing or existing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAddress not found"
        )
    if obj_in.is_default:
        await _clear_default(db, current_user.id, exclude_id=id)
    obj = await crud.user_address_crud.update(db, id, obj_in)
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_addresses(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 - 본인 배송지만 삭제 가능"""
    existing = await crud.user_address_crud.get(db, id)
    if not existing or existing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAddress not found"
        )
    await crud.user_address_crud.delete(db, id)