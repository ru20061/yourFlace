from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.login_logs import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.LoginLogResponse, status_code=status.HTTP_201_CREATED)
async def create_login_logs(
    obj_in: schemas.LoginLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.login_log_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.LoginLogResponse)
async def get_login_logs(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.login_log_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LoginLog not found"
        )
    return obj

@router.get("/", response_model=schemas.LoginLogList)
async def get_login_logs_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    items = await crud.login_log_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.login_log_crud.count(db)
    
    return schemas.LoginLogList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.LoginLogResponse)
async def update_login_logs(
    id: int,
    obj_in: schemas.LoginLogUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.login_log_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LoginLog not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_login_logs(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.login_log_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LoginLog not found"
        )
