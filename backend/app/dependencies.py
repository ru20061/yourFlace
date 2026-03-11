from fastapi import Depends, HTTPException, status, Cookie
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import verify_token
from app.auth.users.crud import user_crud


async def get_current_user(
    access_token: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db)
):
    """HttpOnly 쿠키에서 토큰을 읽어 현재 사용자 조회"""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다",
        )

    payload = verify_token(access_token, "access")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
        )

    user = await user_crud.get(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
        )

    return user


async def get_current_active_user(
    current_user=Depends(get_current_user)
):
    """활성 사용자 확인"""
    if current_user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다",
        )
    return current_user
