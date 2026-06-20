from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.users.model import User


def require_permission(permission_name: str) -> Callable:
    async def _check(current_user: User = Depends(get_current_user)) -> None:
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return _check
