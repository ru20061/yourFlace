from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.chat.chat_rooms import crud, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.ChatRoomResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_rooms(
    obj_in: schemas.ChatRoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.chat_room_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.ChatRoomResponse)
async def get_chat_rooms(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.chat_room_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ChatRoom not found"
        )
    return obj

@router.get("", response_model=schemas.ChatRoomList)
async def get_chat_rooms_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회"""
    items = await crud.chat_room_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.chat_room_crud.count(db)
    
    return schemas.ChatRoomList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.patch("/{id}", response_model=schemas.ChatRoomResponse)
async def update_chat_rooms(
    id: int,
    obj_in: schemas.ChatRoomUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.chat_room_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ChatRoom not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_rooms(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.chat_room_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ChatRoom not found"
        )
