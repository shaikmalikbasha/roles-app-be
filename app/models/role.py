from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.permission import Permission, role_permissions

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    description: str | None = Column(String, nullable=True)

    permissions: list[Permission] = relationship(
        "Permission", secondary=role_permissions, lazy="selectin"
    )
