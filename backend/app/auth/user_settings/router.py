from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.user_settings import crud, schemas
from app.auth.user_settings.models import UserSetting
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=schemas.UserSettingResponse)
async def get_my_settings(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """내 설정 조회 (없으면 기본값으로 자동 생성)"""
    result = await db.execute(
        select(UserSetting).where(UserSetting.user_id == current_user.id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        create_data = schemas.UserSettingCreate(user_id=current_user.id)
        obj = await crud.user_setting_crud.create(db, create_data)
    return obj


@router.patch("/me", response_model=schemas.UserSettingResponse)
async def update_my_settings(
    obj_in: schemas.UserSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """내 설정 저장 (없으면 자동 생성 후 업데이트)"""
    result = await db.execute(
        select(UserSetting).where(UserSetting.user_id == current_user.id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        create_data = schemas.UserSettingCreate(user_id=current_user.id)
        obj = await crud.user_setting_crud.create(db, create_data)
    obj = await crud.user_setting_crud.update(db, obj.id, obj_in)
    return obj


@router.post("", response_model=schemas.UserSettingResponse, status_code=status.HTTP_201_CREATED)
async def create_user_settings(
    obj_in: schemas.UserSettingCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.user_setting_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.UserSettingResponse)
async def get_user_settings(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.user_setting_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserSetting not found"
        )
    return obj

@router.get("", response_model=schemas.UserSettingList)
async def get_user_settings_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    items = await crud.user_setting_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.user_setting_crud.count(db)
    
    return schemas.UserSettingList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.UserSettingResponse)
async def update_user_settings(
    id: int,
    obj_in: schemas.UserSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.user_setting_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserSetting not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_settings(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.user_setting_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserSetting not found"
        )
