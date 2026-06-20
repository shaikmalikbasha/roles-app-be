from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_permission
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from app.services import permission_service

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post(
    "",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("permission:create"))],
)
async def create_permission(
    data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PermissionResponse:
    return await permission_service.create_permission(db, data, current_user.id)


@router.get(
    "",
    response_model=list[PermissionResponse],
    dependencies=[Depends(require_permission("permission:view"))],
)
async def list_permissions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[PermissionResponse]:
    return await permission_service.list_permissions(db, skip=skip, limit=limit)


@router.get(
    "/{perm_id}",
    response_model=PermissionResponse,
    dependencies=[Depends(require_permission("permission:view"))],
)
async def get_permission(
    perm_id: int,
    db: AsyncSession = Depends(get_db),
) -> PermissionResponse:
    return await permission_service.get_permission(db, perm_id)


@router.patch(
    "/{perm_id}",
    response_model=PermissionResponse,
    dependencies=[Depends(require_permission("permission:update"))],
)
async def update_permission(
    perm_id: int,
    data: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PermissionResponse:
    return await permission_service.update_permission(
        db, perm_id, data, current_user.id
    )


@router.delete(
    "/{perm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("permission:delete"))],
)
async def delete_permission(
    perm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    await permission_service.delete_permission(db, perm_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
