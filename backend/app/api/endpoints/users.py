from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User
from app.schemas.responses import UserAdminResponse, UserListResponse, UserResponse, UserMeResponse, UserRolerResponse
from app.schemas.requests import (
    UserChangeRequest,
    UserCreateRequest,
    UserUpdatePasswordRequest,
    BaseUser,
)
from app.core.security import get_password_hash


router = APIRouter()


# ----------------------------- Self -----------------------------
@router.get("/me", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
async def read_current_user(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Get current user"""
    result = await session.execute(select(User).where(User.id == current_user.id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserMeResponse(
        email=user.email,
        phone=user.phone if user.phone else "",
        name=user.name,
        role=user.role,
    )


@router.post(
    "/reset-password", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: BaseUser = Depends(deps.get_current_user),
):
    """Update current user password"""
    current_user.password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return UserMeResponse(
        email=current_user.email,
        phone=current_user.phone if current_user.phone else "",
        name=current_user.name,
        role=current_user.role,
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete current user"""
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()


@router.get("/role", response_model=UserRolerResponse, status_code=status.HTTP_200_OK)
async def get_current_user_role(
    current_user: BaseUser = Depends(deps.get_current_user),
):
    """Get current user role"""
    return UserRolerResponse(role=current_user.role)

# ----------------------------- Admin -----------------------------
@router.get("/all", response_model=UserListResponse)
async def list_users(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """List all users (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    result = await session.execute(select(User))
    users = result.scalars().all()

    all_users = []
    for user in users:
        # print(user.name, user.role)
        if user.role == "admin":
            continue
        all_users.append(
            UserAdminResponse(
                id=user.id,
                email=user.email,
                phone=user.phone if user.phone else "",
                name=user.name,
                role=user.role,
            )
        )
    return UserListResponse(users=all_users)


@router.get("/{id}", response_model=UserAdminResponse, status_code=status.HTTP_200_OK)
async def get_user(
    id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Get a user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    result = await session.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserMeResponse(
        id=user.id,
        email=user.email,
        phone=user.phone if user.phone else "",
        name=user.name,
        role=user.role,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete a user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    await session.execute(delete(User).where(User.id == id))
    await session.commit()
    return


@router.post("/", response_model=UserMeResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreateRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    result = await session.execute(select(User).where(User.email == user.email))
    if result.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        phone=user.phone,
        name=user.name,
        role=user.role,
    )
    session.add(new_user)
    await session.commit()
    return UserMeResponse(
        email=new_user.email,
        phone=new_user.phone if new_user.phone else "",
        name=new_user.name,
        role=new_user.role,
    )


@router.put("/{id}", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
async def update_user(
    id: str,
    new_user: UserChangeRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Update a user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = new_user.email if new_user.email else user.email
    user.phone = new_user.phone if new_user.phone is None else user.phone
    user.name = new_user.name if new_user.name else user.name
    user.role = new_user.role if new_user.role else user.role
    await session.commit()
    return UserMeResponse(
        email=user.email,
        phone=user.phone if user.phone else "",
        name=user.name,
        role=user.role,
    )
