from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import permission_repository
from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)


async def create_permission(
    session: AsyncSession, data: PermissionCreate
) -> PermissionResponse:
    existing = await permission_repository.get_by_name(session, data.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Permission '{data.name}' already exists.",
        )
    permission = await permission_repository.create(
        session, name=data.name, description=data.description
    )
    await session.commit()
    await session.refresh(permission)
    return PermissionResponse.model_validate(permission)


async def list_permissions(session: AsyncSession) -> list[PermissionResponse]:
    permissions = await permission_repository.get_all(session)
    return [PermissionResponse.model_validate(p) for p in permissions]


async def get_permission(
    session: AsyncSession, permission_id: int
) -> PermissionResponse:
    permission = await permission_repository.get_by_id(session, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission_id} not found.",
        )
    return PermissionResponse.model_validate(permission)


async def update_permission(
    session: AsyncSession, permission_id: int, data: PermissionUpdate
) -> PermissionResponse:
    permission = await permission_repository.get_by_id(session, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission_id} not found.",
        )
    fields = data.model_dump(exclude_unset=True)
    if fields:
        if "name" in fields:
            conflict = await permission_repository.get_by_name(session, fields["name"])
            if conflict is not None and conflict.id != permission_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Permission '{fields['name']}' already exists.",
                )
        permission = await permission_repository.update(session, permission, **fields)
    await session.commit()
    await session.refresh(permission)
    return PermissionResponse.model_validate(permission)


async def delete_permission(session: AsyncSession, permission_id: int) -> None:
    permission = await permission_repository.get_by_id(session, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission_id} not found.",
        )
    await permission_repository.delete(session, permission)
    await session.commit()
