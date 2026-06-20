from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.models.role import Role


async def get_by_id(session: AsyncSession, role_id: int) -> Role | None:
    result = await session.execute(select(Role).where(Role.id == role_id))
    return result.scalar_one_or_none()


async def get_by_name(session: AsyncSession, name: str) -> Role | None:
    result = await session.execute(select(Role).where(Role.name == name))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[Role]:
    result = await session.execute(select(Role))
    return list(result.scalars().all())


async def create(
    session: AsyncSession, name: str, description: str | None = None
) -> Role:
    role = Role(name=name, description=description)
    session.add(role)
    await session.flush()
    await session.refresh(role)
    return role


async def update(session: AsyncSession, role: Role, **fields) -> Role:
    for key, value in fields.items():
        setattr(role, key, value)
    await session.flush()
    await session.refresh(role)
    return role


async def delete(session: AsyncSession, role: Role) -> None:
    await session.delete(role)
    await session.flush()


async def assign_permission(
    session: AsyncSession, role: Role, permission: Permission
) -> None:
    if permission not in role.permissions:
        role.permissions.append(permission)
        await session.flush()


async def remove_permission(
    session: AsyncSession, role: Role, permission: Permission
) -> None:
    role.permissions.remove(permission)
    await session.flush()
