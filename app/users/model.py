from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import BaseMixin
from app.core.database import Base
from app.roles.model import Role, user_roles


class User(BaseMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    roles: Mapped[list[Role]] = relationship(secondary=user_roles, lazy="selectin")
