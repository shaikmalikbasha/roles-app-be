from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.user import User


async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())


async def create(session: AsyncSession, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def update(session: AsyncSession, user: User, **fields) -> User:
    for key, value in fields.items():
        setattr(user, key, value)
    await session.flush()
    await session.refresh(user)
    return user


async def delete(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.flush()


async def assign_role(session: AsyncSession, user: User, role: Role) -> None:
    if role not in user.roles:
        user.roles.append(role)
        await session.flush()


async def remove_role(session: AsyncSession, user: User, role: Role) -> None:
    user.roles.remove(role)
    await session.flush()
