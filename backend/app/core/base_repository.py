from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_model import BaseMixin

ModelT = TypeVar("ModelT", bound=BaseMixin)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelT | None:
        result = await session.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelT]:
        result = await session.execute(
            select(self.model)
            .where(self.model.is_deleted == False)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
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

    async def delete(
        self, session: AsyncSession, instance: ModelT, updated_by: int = 0
    ) -> None:
        instance.is_deleted = True
        instance.updated_by = updated_by
        await session.flush()
