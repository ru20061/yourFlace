from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, Cookie
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.config import settings
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

ACCESS_MAX_AGE  = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_MAX_AGE = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """액세스/리프레시 토큰을 HttpOnly 쿠키로 설정"""
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,   # 운영 환경에서는 True (HTTPS)
        max_age=ACCESS_MAX_AGE,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=REFRESH_MAX_AGE,
        path="/",
    )


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


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(body: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    """회원가입: 유저 + 프로필 생성 → HttpOnly 쿠키로 JWT 발급"""
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

    # HttpOnly 쿠키로 토큰 발급
    token_data = {"sub": str(user.id)}
    _set_auth_cookies(
        response,
        create_access_token(token_data),
        create_refresh_token(token_data),
    )
    return {"message": "회원가입 성공"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    """로그인: 이메일/비밀번호 검증 → HttpOnly 쿠키로 JWT 발급"""
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
    _set_auth_cookies(
        response,
        create_access_token(token_data),
        create_refresh_token(token_data),
    )
    return {"message": "로그인 성공"}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    """토큰 갱신: refresh_token 쿠키 → 새 access_token + refresh_token 쿠키"""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="리프레시 토큰이 없습니다",
        )

    payload = verify_token(refresh_token, token_type="refresh")

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
    _set_auth_cookies(
        response,
        create_access_token(token_data),
        create_refresh_token(token_data),
    )
    return {"message": "토큰 갱신 성공"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    """로그아웃: 쿠키 삭제"""
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "로그아웃 성공"}


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
