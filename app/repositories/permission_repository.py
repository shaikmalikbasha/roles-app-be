from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.models.permission import Permission


class PermissionRepository(BaseRepository[Permission]):
    model = Permission

    async def get_by_name(self, session: AsyncSession, name: str) -> Permission | None:
        result = await session.execute(
            select(Permission).where(
                Permission.name == name,
                Permission.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()


permission_repository = PermissionRepository()
