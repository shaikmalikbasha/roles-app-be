from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories import role_repository, user_repository
from app.schemas.user import UserCreate, UserResponse, UserUpdate


async def create_user(session: AsyncSession, data: UserCreate) -> UserResponse:
    existing = await user_repository.get_by_email(session, data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )
    hashed = hash_password(data.password)
    user = await user_repository.create(
        session, email=data.email, hashed_password=hashed
    )
    await session.commit()
    return UserResponse.model_validate(user)


async def list_users(session: AsyncSession) -> list[UserResponse]:
    users = await user_repository.get_all(session)
    return [UserResponse.model_validate(u) for u in users]


async def get_user(session: AsyncSession, user_id: int) -> UserResponse:
    user = await user_repository.get_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return UserResponse.model_validate(user)


async def update_user(
    session: AsyncSession, user_id: int, data: UserUpdate
) -> UserResponse:
    user = await user_repository.get_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    fields = data.model_dump(exclude_unset=True)
    if "password" in fields:
        fields["hashed_password"] = hash_password(fields.pop("password"))
    await user_repository.update(session, user, **fields)
    await session.commit()
    return UserResponse.model_validate(user)


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await user_repository.get_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    await user_repository.delete(session, user)
    await session.commit()


async def assign_role_to_user(
    session: AsyncSession, user_id: int, role_id: int
) -> None:
    user = await user_repository.get_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found",
        )
    await user_repository.assign_role(session, user, role)
    await session.commit()


async def remove_role_from_user(
    session: AsyncSession, user_id: int, role_id: int
) -> None:
    user = await user_repository.get_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found",
        )
    await user_repository.remove_role(session, user, role)
    await session.commit()
