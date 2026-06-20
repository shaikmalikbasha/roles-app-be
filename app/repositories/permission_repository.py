from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission


async def get_by_id(session: AsyncSession, permission_id: int) -> Permission | None:
    result = await session.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    return result.scalar_one_or_none()


async def get_by_name(session: AsyncSession, name: str) -> Permission | None:
    result = await session.execute(select(Permission).where(Permission.name == name))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[Permission]:
    result = await session.execute(select(Permission))
    return list(result.scalars().all())


async def create(
    session: AsyncSession, name: str, description: str | None = None
) -> Permission:
    permission = Permission(name=name, description=description)
    session.add(permission)
    await session.flush()
    await session.refresh(permission)
    return permission


async def update(session: AsyncSession, permission: Permission, **fields) -> Permission:
    for key, value in fields.items():
        setattr(permission, key, value)
    await session.flush()
    await session.refresh(permission)
    return permission


async def delete(session: AsyncSession, permission: Permission) -> None:
    await session.delete(permission)
    await session.flush()
