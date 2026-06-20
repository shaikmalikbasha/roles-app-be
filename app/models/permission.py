from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import BaseMixin

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class Permission(BaseMixin, Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column()
