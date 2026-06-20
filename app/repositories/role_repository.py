from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.models.permission import Permission
from app.models.role import Role


class RoleRepository(BaseRepository[Role]):
    model = Role

    async def get_by_name(self, session: AsyncSession, name: str) -> Role | None:
        result = await session.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    async def assign_permission(
        self, session: AsyncSession, role: Role, permission: Permission
    ) -> None:
        if permission not in role.permissions:
            role.permissions.append(permission)
            await session.flush()

    async def remove_permission(
        self, session: AsyncSession, role: Role, permission: Permission
    ) -> None:
        role.permissions.remove(permission)
        await session.flush()


role_repository = RoleRepository()
