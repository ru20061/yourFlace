from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.content.artist_images import crud, schemas
from app.subscription.subscriptions.models import Subscription
from app.artist.artists.models import Artist
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.ArtistImageResponse, status_code=status.HTTP_201_CREATED)
async def create_artist_images(
    obj_in: schemas.ArtistImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.artist_image_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.ArtistImageResponse)
async def get_artist_images(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회"""
    obj = await crud.artist_image_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistImage not found"
        )
    return obj

@router.get("", response_model=schemas.ArtistImageListWithAuthor)
async def get_artist_images_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회 (구독 닉네임 포함)"""
    items = await crud.artist_image_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.artist_image_crud.count(db)

    result_items = []
    for img in items:
        author_name = None
        author_profile_image = None

        if img.write_role == "manager":
            # 매니저 → subscription의 fan_nickname 사용
            stmt = select(Subscription.fan_nickname, Subscription.fan_profile_image).where(
                and_(
                    Subscription.fan_id == img.write_id,
                    Subscription.artist_id == img.artist_id,
                    Subscription.status != 'D',
                )
            )
            sub_result = await db.execute(stmt)
            sub = sub_result.first()
            if sub:
                author_name = sub.fan_nickname
                author_profile_image = sub.fan_profile_image
        else:
            # 아티스트 → artist의 stage_name, profile_image 사용
            stmt = select(Artist.stage_name, Artist.profile_image).where(
                Artist.user_id == img.write_id
            )
            artist_result = await db.execute(stmt)
            artist_row = artist_result.first()
            if artist_row:
                author_name = artist_row.stage_name
                author_profile_image = artist_row.profile_image

        img_dict = schemas.ArtistImageResponse.model_validate(img).model_dump()
        img_dict["author_name"] = author_name
        img_dict["author_profile_image"] = author_profile_image
        result_items.append(img_dict)

    return schemas.ArtistImageListWithAuthor(
        items=result_items,
        total=total,
        skip=skip,
        limit=limit,
    )

@router.patch("/{id}", response_model=schemas.ArtistImageResponse)
async def update_artist_images(
    id: int,
    obj_in: schemas.ArtistImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.artist_image_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistImage not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist_images(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.artist_image_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ArtistImage not found"
        )
