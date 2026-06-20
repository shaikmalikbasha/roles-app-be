"""
Seed script — inserts an admin user with full RBAC coverage so you can
log in via Swagger (/docs) and exercise every endpoint immediately.

Usage:
    python ingest.py

What it creates (idempotent — re-running is safe):
  Permissions : all resource:action pairs for users / roles / permissions
  Role        : "admin" with every permission attached
  User        : admin@example.com  /  password: Admin@1234
"""

import asyncio
import logging

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, create_all_tables
from app.core.security import hash_password
from app.permissions.model import Permission
from app.roles.model import Role
from app.users.model import User

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

PERMISSIONS: list[tuple[str, str]] = [
    ("user:create", "Create a new user"),
    ("user:read", "Read user details"),
    ("user:update", "Update an existing user"),
    ("user:delete", "Delete a user"),
    ("role:create", "Create a new role"),
    ("role:read", "Read role details"),
    ("role:update", "Update an existing role"),
    ("role:delete", "Delete a role"),
    ("permission:create", "Create a new permission"),
    ("permission:read", "Read permission details"),
    ("permission:update", "Update an existing permission"),
    ("permission:delete", "Delete a permission"),
]

ADMIN_ROLE = ("admin", "Super-administrator with all permissions")

ADMIN_USER = {
    "email": "admin@example.com",
    "password": "Admin@1234",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _get_or_create_permission(session, name: str, description: str) -> Permission:
    result = await session.execute(select(Permission).where(Permission.name == name))
    perm = result.scalar_one_or_none()
    if perm is None:
        perm = Permission(name=name, description=description)
        session.add(perm)
        await session.flush()
        log.info("  created permission: %s", name)
    return perm


async def _get_or_create_role(session, name: str, description: str) -> Role:
    result = await session.execute(select(Role).where(Role.name == name))
    role = result.scalar_one_or_none()
    if role is None:
        role = Role(name=name, description=description)
        session.add(role)
        await session.flush()
        log.info("  created role: %s", name)
    return role


async def _get_or_create_user(session, email: str, password: str) -> User:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(email=email, hashed_password=hash_password(password), is_active=True)
        session.add(user)
        await session.flush()
        log.info("  created user: %s", email)
    return user


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def seed() -> None:
    log.info("Ensuring tables exist …")
    await create_all_tables()

    async with AsyncSessionLocal() as session:
        # 1. Permissions
        log.info("Seeding permissions …")
        perms: list[Permission] = []
        for name, desc in PERMISSIONS:
            perms.append(await _get_or_create_permission(session, name, desc))

        # 2. Admin role
        log.info("Seeding admin role …")
        role_name, role_desc = ADMIN_ROLE
        admin_role = await _get_or_create_role(session, role_name, role_desc)

        # Attach any missing permissions to the role
        existing_perm_ids = {p.id for p in admin_role.permissions}
        for perm in perms:
            if perm.id not in existing_perm_ids:
                admin_role.permissions.append(perm)
                log.info("  attached %s → %s", perm.name, admin_role.name)

        # 3. Admin user
        log.info("Seeding admin user …")
        admin_user = await _get_or_create_user(
            session, ADMIN_USER["email"], ADMIN_USER["password"]
        )

        # Attach role if missing
        existing_role_ids = {r.id for r in admin_user.roles}
        if admin_role.id not in existing_role_ids:
            admin_user.roles.append(admin_role)
            log.info("  attached role '%s' → user '%s'", admin_role.name, admin_user.email)

        await session.commit()

    log.info("")
    log.info("Done. You can now log in via Swagger at /docs")
    log.info("  email   : %s", ADMIN_USER["email"])
    log.info("  password: %s", ADMIN_USER["password"])


if __name__ == "__main__":
    asyncio.run(seed())
