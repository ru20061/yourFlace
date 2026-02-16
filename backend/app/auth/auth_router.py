from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.auth.users.models import User
from app.auth.profile.models import Profile
from app.dependencies import get_current_user

router = APIRouter()


# ── Schemas ──

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Literal["male", "female"]] = None
    phone: Optional[str] = None


class CheckEmailResponse(BaseModel):
    available: bool
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    email: str
    nickname: Optional[str] = None
    profile_image: Optional[str] = None


# ── Endpoints ──

@router.get("/check-email", response_model=CheckEmailResponse)
async def check_email(
    email: EmailStr = Query(..., description="중복 확인할 이메일"),
    db: AsyncSession = Depends(get_db),
):
    """이메일 중복 확인"""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    if result.scalar_one_or_none():
        return CheckEmailResponse(available=False, message="이미 등록된 이메일입니다")
    return CheckEmailResponse(available=True, message="사용 가능한 이메일입니다")


@router.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """회원가입: 유저 + 프로필 생성 → JWT 토큰 반환"""
    # 이메일 중복 확인
    existing = await db.execute(
        select(User).where(User.email == body.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 이메일입니다",
        )

    # 유저 생성
    user = User(
        email=body.email,
        password_hash=get_password_hash(body.password),
        status="active",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    # 프로필 생성
    profile = Profile(
        user_id=user.id,
        nickname=body.nickname,
        full_name=body.full_name,
        birth_date=body.birth_date,
        gender=body.gender,
        phone=body.phone,
    )
    db.add(profile)
    await db.flush()

    # 토큰 발급
    token_data = {"sub": str(user.id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """로그인: 이메일/비밀번호 검증 → JWT 토큰 반환"""
    result = await db.execute(
        select(User).where(User.email == body.email, User.status != "D")
    )
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
        )

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
        )

    token_data = {"sub": str(user.id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """토큰 갱신: refresh_token → 새 access_token + refresh_token"""
    payload = verify_token(body.refresh_token, token_type="refresh")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
        )

    # 유저 존재 확인
    result = await db.execute(
        select(User).where(User.id == int(user_id), User.status != "D")
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
        )

    token_data = {"sub": user_id}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.get("/me", response_model=MeResponse)
async def me(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """현재 로그인된 유저 정보"""
    result = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        nickname=profile.nickname if profile else None,
        profile_image=profile.profile_image if profile else None,
    )
