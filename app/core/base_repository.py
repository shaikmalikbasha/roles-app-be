from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_model import BaseMixin

ModelT = TypeVar("ModelT", bound=BaseMixin)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelT | None:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> list[ModelT]:
        result = await session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, **fields) -> ModelT:
        instance = self.model(**fields)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def update(self, session: AsyncSession, instance: ModelT, **fields) -> ModelT:
        for key, value in fields.items():
            setattr(instance, key, value)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, instance: ModelT) -> None:
        await session.delete(instance)
        await session.flush()
