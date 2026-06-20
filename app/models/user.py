from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.role import Role, user_roles


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    roles: list[Role] = relationship("Role", secondary=user_roles, lazy="selectin")
