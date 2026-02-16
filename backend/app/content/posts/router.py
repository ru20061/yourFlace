from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, and_, func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.content.posts import crud, schemas
from app.content.posts.models import Post
from app.subscription.subscriptions.models import Subscription
from app.artist.artists.models import Artist
from app.auth.profile.models import Profile
from app.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_posts(
    obj_in: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """생성"""
    obj = await crud.post_crud.create(db, obj_in)
    return obj

@router.get("/{id}", response_model=schemas.PostWithAuthor)
async def get_posts(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """단건 조회 (구독 닉네임 포함)"""
    obj = await crud.post_crud.get(db, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    author_name, author_profile_image = await _resolve_author(db, obj)
    post_dict = schemas.PostResponse.model_validate(obj).model_dump()
    post_dict["author_name"] = author_name
    post_dict["author_profile_image"] = author_profile_image
    return post_dict


async def _resolve_author(db: AsyncSession, post) -> tuple:
    """포스트 작성자 이름/이미지 조회: 팬→구독닉네임(활성)→프로필, 아티스트→stage_name"""
    if post.write_role == "fan":
        # 1) 활성 구독의 fan_nickname 우선 (status='subscribed'만, 최신 우선)
        stmt = (
            select(Subscription.fan_nickname, Subscription.fan_profile_image)
            .where(
                and_(
                    Subscription.fan_id == post.write_id,
                    Subscription.artist_id == post.author_id,
                    Subscription.status == 'subscribed',
                )
            )
            .order_by(Subscription.created_at.desc())
            .limit(1)
        )
        sub_row = (await db.execute(stmt)).first()

        if sub_row and sub_row.fan_nickname:
            return sub_row.fan_nickname, sub_row.fan_profile_image

        # 2) 구독 닉네임 없으면 프로필 fallback
        stmt = select(Profile.nickname, Profile.full_name, Profile.profile_image).where(
            Profile.user_id == post.write_id
        )
        profile_row = (await db.execute(stmt)).first()
        if profile_row:
            name = profile_row.nickname or profile_row.full_name
            image = (sub_row.fan_profile_image if sub_row and sub_row.fan_profile_image else None) or profile_row.profile_image
            return name, image
        return None, None
    else:
        # 아티스트/매니저 → Artist.stage_name
        stmt = select(Artist.stage_name, Artist.profile_image).where(
            Artist.user_id == post.write_id
        )
        artist_row = (await db.execute(stmt)).first()
        if artist_row:
            return artist_row.stage_name, artist_row.profile_image
        return None, None


@router.get("", response_model=schemas.PostListWithAuthor)
async def get_posts_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """목록 조회 (구독 닉네임 포함)"""
    items = await crud.post_crud.get_multi(db, skip=skip, limit=limit)
    total = await crud.post_crud.count(db)

    result_items = []
    for post in items:
        author_name, author_profile_image = await _resolve_author(db, post)
        post_dict = schemas.PostResponse.model_validate(post).model_dump()
        post_dict["author_name"] = author_name
        post_dict["author_profile_image"] = author_profile_image
        result_items.append(post_dict)

    return schemas.PostListWithAuthor(
        items=result_items,
        total=total,
        skip=skip,
        limit=limit,
    )

@router.patch("/{id}", response_model=schemas.PostResponse)
async def update_posts(
    id: int,
    obj_in: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """업데이트"""
    obj = await crud.post_crud.update(db, id, obj_in)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """삭제 (status='D')"""
    success = await crud.post_crud.delete(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
