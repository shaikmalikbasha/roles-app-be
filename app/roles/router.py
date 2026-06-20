from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_permission
from app.roles import service as role_service
from app.roles.schemas import RoleCreate, RoleResponse, RoleUpdate
from app.users.model import User

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("role:create"))],
)
async def create_role(
    data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RoleResponse:
    return await role_service.create_role(db, data, current_user.id)


@router.get(
    "",
    response_model=list[RoleResponse],
    dependencies=[Depends(require_permission("role:view"))],
)
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[RoleResponse]:
    return await role_service.list_roles(db, skip=skip, limit=limit)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(require_permission("role:view"))],
)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
) -> RoleResponse:
    return await role_service.get_role(db, role_id)


@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(require_permission("role:update"))],
)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RoleResponse:
    return await role_service.update_role(db, role_id, data, current_user.id)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("role:delete"))],
)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    await role_service.delete_role(db, role_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{role_id}/permissions/{perm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("role:update"))],
)
async def assign_permission_to_role(
    role_id: int,
    perm_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    await role_service.assign_permission_to_role(db, role_id, perm_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{role_id}/permissions/{perm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("role:update"))],
)
async def remove_permission_from_role(
    role_id: int,
    perm_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    await role_service.remove_permission_from_role(db, role_id, perm_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
