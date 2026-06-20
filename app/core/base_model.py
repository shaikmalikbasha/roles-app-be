from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BaseMixin:
    __mapper_args__ = {"always_refresh": True}

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    created_by: Mapped[int] = mapped_column(default=0)
    updated_by: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=_utcnow, onupdate=_utcnow)
    is_deleted: Mapped[bool] = mapped_column(default=False)
