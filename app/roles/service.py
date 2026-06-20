from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.permissions.repository import permission_repository
from app.roles.repository import role_repository
from app.roles.schemas import RoleCreate, RoleResponse, RoleUpdate


async def create_role(
    session: AsyncSession, data: RoleCreate, current_user_id: int = 0
) -> RoleResponse:
    existing = await role_repository.get_by_name(session, data.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role '{data.name}' already exists.",
        )
    role = await role_repository.create(
        session,
        name=data.name,
        description=data.description,
        created_by=current_user_id,
        updated_by=current_user_id,
    )
    await session.commit()
    await session.refresh(role)
    return RoleResponse.model_validate(role)


async def list_roles(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[RoleResponse]:
    roles = await role_repository.get_all(session, skip=skip, limit=limit)
    return [RoleResponse.model_validate(r) for r in roles]


async def get_role(session: AsyncSession, role_id: int) -> RoleResponse:
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found.",
        )
    return RoleResponse.model_validate(role)


async def update_role(
    session: AsyncSession, role_id: int, data: RoleUpdate, current_user_id: int = 0
) -> RoleResponse:
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found.",
        )
    fields = data.model_dump(exclude_unset=True)
    if fields:
        if "name" in fields:
            conflict = await role_repository.get_by_name(session, fields["name"])
            if conflict is not None and conflict.id != role_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Role '{fields['name']}' already exists.",
                )
        fields["updated_by"] = current_user_id
        role = await role_repository.update(session, role, **fields)
    await session.commit()
    await session.refresh(role)
    return RoleResponse.model_validate(role)


async def delete_role(
    session: AsyncSession, role_id: int, current_user_id: int = 0
) -> None:
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found.",
        )
    await role_repository.delete(session, role, updated_by=current_user_id)
    await session.commit()


async def assign_permission_to_role(
    session: AsyncSession, role_id: int, permission_id: int
) -> None:
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found.",
        )
    permission = await permission_repository.get_by_id(session, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission_id} not found.",
        )
    await role_repository.assign_permission(session, role, permission)
    await session.commit()


async def remove_permission_from_role(
    session: AsyncSession, role_id: int, permission_id: int
) -> None:
    role = await role_repository.get_by_id(session, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {role_id} not found.",
        )
    permission = await permission_repository.get_by_id(session, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission_id} not found.",
        )
    await role_repository.remove_permission(session, role, permission)
    await session.commit()
