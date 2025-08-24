import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import config, security
from app.models import User
from app.schemas.requests import (
    UserCreateRequest,
)
from app.schemas.requests import UserLoginRequest
from app.schemas.responses import AccessTokenResponse, UserResponse
from app.core.security import get_password_hash
from app.core.security import create_jwt_token

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new user"""
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
    user = User(
        email=new_user.email,
        password=get_password_hash(new_user.password),
        phone=new_user.phone if new_user.phone else "",
        name=new_user.name,
        role=new_user.role,
    )
    session.add(user)
    await session.commit()
    return UserResponse(status="success", token=security.create_jwt_token(new_user.email, new_user.password))


@router.post("/login", response_model=UserResponse, status_code=200)
async def login_user(
    user: UserLoginRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Login user"""
    result = await session.execute(select(User).where(User.email == user.email))
    fetch_user = result.scalars().first()
    if fetch_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not security.verify_password(user.password, fetch_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")
    return UserResponse(status="success", token=security.create_jwt_token(user.email, user.password))


@router.get("/validate-token", response_model=UserResponse, status_code=200)
async def validate_token(
    token: str,
    session: AsyncSession = Depends(deps.get_session),
):
    """Validate token"""
    try:
        payload = jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.email == token_data.email))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "success", "token": token}
