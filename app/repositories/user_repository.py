from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.models.role import Role
from app.models.user import User


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def assign_role(self, session: AsyncSession, user: User, role: Role) -> None:
        if role not in user.roles:
            user.roles.append(role)
            await session.flush()

    async def remove_role(self, session: AsyncSession, user: User, role: Role) -> None:
        user.roles.remove(role)
        await session.flush()


user_repository = UserRepository()
