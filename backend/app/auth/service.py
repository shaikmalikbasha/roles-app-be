from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import LoginRequest, MeResponse, TokenResponse
from app.core.security import create_access_token, verify_password
from app.users.model import User
from app.users.repository import user_repository


async def login(session: AsyncSession, data: LoginRequest) -> TokenResponse:
    user = await user_repository.get_by_email(session, data.email)
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return TokenResponse(access_token=create_access_token(user.id))


async def get_me(session: AsyncSession, current_user: User) -> MeResponse:
    roles = [r.name for r in current_user.roles]
    permissions = list({p.name for r in current_user.roles for p in r.permissions})
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        roles=roles,
        permissions=permissions,
    )
